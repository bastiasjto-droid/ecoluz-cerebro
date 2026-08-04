import streamlit as st
import pandas as pd
import io
import datetime
import json

# --- CONFIGURACIÓN DE DISEÑO ---
st.set_page_config(page_title="ECOLUZ Inspector", layout="wide", page_icon="🧠")

# --- ESTADO DE LA SESIÓN ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 0 
if 'proyecto' not in st.session_state:
    st.session_state.proyecto = None
if 'partidas_seleccionadas' not in st.session_state:
    st.session_state.partidas_seleccionadas = []
if 'partida_actual_idx' not in st.session_state:
    st.session_state.partida_actual_idx = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}
if 'materiales_totales' not in st.session_state:
    st.session_state.materiales_totales = []

# --- 1. BIBLIOTECA DE PARTIDAS ---
BIBLIOTECA_PARTIDAS = {
    "Remodelación": {
        "Cocina": {
            "Muros": {
                "descripcion": "Levantamiento de muros de cocina",
                "preguntas": [
                    {"id": "mu_mat", "pregunta": "Material del muro:", "tipo": "select", "opciones": ["Ladrillo", "Metalcon", "Hormigón"]},
                    {"id": "mu_estado", "pregunta": "Estado actual del muro:", "tipo": "select", "opciones": ["Bueno", "Regular", "Malo"]},
                    {"id": "mu_humedad", "pregunta": "¿Hay humedad visible?", "tipo": "bool"},
                    {"id": "mu_m2", "pregunta": "Metros cuadrados (m²) del muro:", "tipo": "float"}
                ],
                "reglas": {
                    "mu_humedad": {
                        True: {"accion": "agregar_material", "material": "Impermeabilizante", "unidad": "unid"}
                    }
                }
            },
            "Pisos": {
                "descripcion": "Levantamiento de pisos",
                "preguntas": [
                    {"id": "pi_tipo", "pregunta": "Tipo de piso a instalar:", "tipo": "select", "opciones": ["Cerámica", "Porcelanato", "Vinílico"]},
                    {"id": "pi_m2", "pregunta": "Metros cuadrados aproximados (m²):", "tipo": "float"},
                    {"id": "pi_fecha", "pregunta": "Fecha estimada de inicio de la obra:", "tipo": "date"}
                ],
                "reglas": {}
            }
        }
    }
}

# --- 2. MOTOR INTELIGENTE DE PREGUNTAS ---
def renderizar_pregunta(config):
    """
    Esta función revisa el 'tipo' de la pregunta y dibuja el componente correcto.
    """
    tipo = config.get("tipo", "text") # Por defecto, si no tiene tipo, es texto
    
    try:
        if tipo == "text":
            return st.text_input(config["pregunta"])
        elif tipo == "int":
            return st.number_input(config["pregunta"], value=0, step=1)
        elif tipo == "float":
            return st.number_input(config["pregunta"], value=0.0, step=0.1)
        elif tipo == "bool":
            return st.radio(config["pregunta"], ["Sí", "No"]) == "Sí" # Devuelve True o False
        elif tipo == "select":
            return st.selectbox(config["pregunta"], config["opciones"])
        elif tipo == "multiselect":
            return st.multiselect(config["pregunta"], config["opciones"])
        elif tipo == "date":
            return st.date_input(config["pregunta"], value=datetime.date.today())
        else:
            return st.text_input(config["pregunta"])
    except Exception as e:
        st.error(f"Error mostrando la pregunta '{config['pregunta']}': {e}")
        return None

# --- 3. NAVEGACIÓN ---
etapa = st.session_state.etapa

# ETAPA 0: INICIO
if etapa == 0:
    st.title("🧠 INSPECTOR TÉCNICO ECOLUZ")
    st.subheader("¿Qué tipo de proyecto realizará?")
    col1, col2 = st.columns(2)
    if col1.button("🏠 Remodelación"):
        st.session_state.proyecto = "Remodelación"
        st.session_state.etapa = 1
        st.rerun()
    if col2.button("📐 Ampliación"):
        st.session_state.proyecto = "Ampliación"
        st.session_state.etapa = 1
        st.rerun()

# ETAPA 1: SELECCIÓN DE PARTIDAS
elif etapa == 1:
    st.subheader(f"Seleccione las partidas a intervenir para {st.session_state.proyecto}")
    proyecto_data = BIBLIOTECA_PARTIDAS[st.session_state.proyecto]
    partidas = []
    for recinto, elementos in proyecto_data.items():
        for elemento in elementos.keys():
            partidas.append(f"{recinto} - {elemento}")
    
    st.session_state.partidas_seleccionadas = st.multiselect("Partidas a intervenir:", partidas)
    
    if st.button("Iniciar Levantamiento Técnico"):
        if st.session_state.partidas_seleccionadas:
            st.session_state.etapa = 2
            st.rerun()
        else:
            st.warning("Selecciona al menos una partida.")

# ETAPA 2: LEVANTAMIENTO
elif etapa == 2:
    idx_actual = st.session_state.partida_actual_idx
    
    if idx_actual < len(st.session_state.partidas_seleccionadas):
        partida_nombre = st.session_state.partidas_seleccionadas[idx_actual]
        recinto, elemento = partida_nombre.split(" - ")
        config_partida = BIBLIOTECA_PARTIDAS[st.session_state.proyecto][recinto][elemento]
        
        st.subheader(f"📋 Levantando: {partida_nombre}")
        st.caption(config_partida["descripcion"])
        
        # Aquí está la corrección CRUCIAL: El botón submit DENTRO del formulario
        with st.form(key=f"form_{idx_actual}"):
            respuestas_temp = {}
            
            for pregunta in config_partida["preguntas"]:
                # Usamos el motor inteligente para dibujar la pregunta
                respuesta = renderizar_pregunta(pregunta)
                if respuesta is not None:
                    respuestas_temp[pregunta["id"]] = respuesta
            
            # BOTÓN DE ENVÍO DEL FORMULARIO (Corrección #1)
            enviado = st.form_submit_button("✅ Finalizar esta partida")
        
        # Procesar solo si se presionó el botón
        if enviado:
            # Guardar respuestas
            st.session_state.respuestas[partida_nombre] = respuestas_temp
            
            # Procesar reglas y generar materiales
            for p_id, respuesta in respuestas_temp.items():
                if p_id in config_partida["reglas"]:
                    regla = config_partida["reglas"][p_id]
                    if respuesta in regla:
                        accion = regla[respuesta]
                        if accion["accion"] == "agregar_material":
                            st.session_state.materiales_totales.append({
                                "Partida": partida_nombre,
                                "Material": accion["material"],
                                "Unidad": accion["unidad"],
                                "Cantidad": "Por calcular" 
                            })
                            
            # Avanzar
            st.session_state.partida_actual_idx += 1
            st.rerun()
    else:
        st.session_state.etapa = 3
        st.rerun()

# ETAPA 3: FINAL
elif etapa == 3:
    st.balloons()
    st.success("🎉 ¡Levantamiento técnico completado!")
    
    # Generar Excel
    df = pd.DataFrame(st.session_state.materiales_totales)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MATERIALES')
    
    st.download_button(
        label="📥 DESCARGAR EXCEL CON MATERIALES (.xlsx)",
        data=output.getvalue(),
        file_name=f"Materiales_ECOLUZ_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    )
    
    if st.button("🔄 Iniciar nuevo proyecto"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
