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
if 'especificacion_texto' not in st.session_state:
    st.session_state.especificacion_texto = []

# --- 1. BIBLIOTECA DE PARTIDAS (El Cerebro Modular) ---
# Aquí es donde agregarás nuevas "Partidas" sin tocar el motor.
BIBLIOTECA_PARTIDAS = {
    "Remodelación": {
        "Cocina": {
            "Muros": {
                "descripcion": "Levantamiento de muros de cocina",
                "preguntas": [
                    {"id": "mu_mat", "pregunta": "Material del muro:", "opciones": ["Ladrillo", "Metalcon", "Hormigón"]},
                    {"id": "mu_estado", "pregunta": "Estado actual:", "opciones": ["Bueno", "Regular", "Malo"]},
                    {"id": "mu_humedad", "pregunta": "¿Hay humedad visible?", "opciones": ["Sí", "No"]},
                    {"id": "mu_revest", "pregunta": "Revestimiento final:", "opciones": ["Cerámica", "Pintura", "Estuco"]}
                ],
                "reglas": {
                    "mu_humedad": {
                        "Sí": {"accion": "agregar_material", "material": "Impermeabilizante", "unidad": "unid"}
                    }
                }
            },
            "Pisos": {
                "descripcion": "Levantamiento de pisos",
                "preguntas": [
                    {"id": "pi_tipo", "pregunta": "Tipo de piso a instalar:", "opciones": ["Cerámica", "Porcelanato", "Vinílico"]},
                    {"id": "pi_m2", "pregunta": "Metros cuadrados aproximados (m²):", "tipo": "numero"}
                ],
                "reglas": {}
            }
        },
        "Baño": {
            "Pisos": {
                "descripcion": "Levantamiento de pisos de baño",
                "preguntas": [
                    {"id": "ba_pi_tipo", "pregunta": "Tipo de piso a instalar:", "opciones": ["Cerámica", "Porcelanato"]},
                    {"id": "ba_pi_imper", "pregunta": "¿Requiere impermeabilización bajo el piso?", "opciones": ["Sí", "No"]}
                ],
                "reglas": {
                    "ba_pi_imper": {
                        "Sí": {"accion": "agregar_material", "material": "Membrana impermeabilizante", "unidad": "m2"}
                    }
                }
            }
        }
    },
    "Ampliación": {
        "Nuevo Recinto": {
            "Fundaciones": {
                "descripcion": "Levantamiento de fundaciones",
                "preguntas": [
                    {"id": "amp_fund", "pregunta": "Tipo de fundación:", "opciones": ["Corrida", "Aislada", "Losa"]},
                    {"id": "amp_excav", "pregunta": "Profundidad de excavación (metros):", "tipo": "numero"}
                ],
                "reglas": {}
            }
        }
    }
}

# --- 2. MOTOR DE NAVEGACIÓN ---
etapa = st.session_state.etapa

# ETAPA 0: INICIO (Selección de proyecto)
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

# ETAPA 1: SELECCIÓN DE PARTIDAS (Recintos y Elementos)
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

# ETAPA 2: LEVANTAMIENTO (Árbol de preguntas por partida)
elif etapa == 2:
    idx_actual = st.session_state.partida_actual_idx
    
    if idx_actual < len(st.session_state.partidas_seleccionadas):
        partida_nombre = st.session_state.partidas_seleccionadas[idx_actual]
        recinto, elemento = partida_nombre.split(" - ")
        
        # Obtener la configuración de la partida
        config_partida = BIBLIOTECA_PARTIDAS[st.session_state.proyecto][recinto][elemento]
        st.subheader(f"📋 Levantando: {partida_nombre}")
        st.write(config_partida["descripcion"])
        
        # Formulario de preguntas
        with st.form(f"form_{idx_actual}"):
            respuestas_temp = {}
            for pregunta in config_partida["preguntas"]:
                if pregunta.get("tipo") == "numero":
                    respuestas_temp[pregunta["id"]] = st.number_input(pregunta["pregunta"], min_value=0, step=1.0)
                else:
                    respuestas_temp[pregunta["id"]] = st.radio(pregunta["pregunta"], pregunta["opciones"])
            
            if st.form_submit_button("✅ Finalizar esta partida"):
                # Guardar respuestas
                st.session_state.respuestas[partida_nombre] = respuestas_temp
                
                # Procesar reglas y generar materiales automáticamente
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
                                
                # Avanzar a la siguiente partida
                st.session_state.partida_actual_idx += 1
                st.rerun()
    else:
        # Si ya no hay más partidas, pasar al final
        st.session_state.etapa = 3
        st.rerun()

# ETAPA 3: FINALIZACIÓN
elif etapa == 3:
    st.balloons()
    st.success("🎉 ¡Levantamiento técnico completado!")
    st.subheader("📄 Generando Especificación y Listado de Materiales")
    
    # --- GENERAR EXCEL DE MATERIALES ---
    df = pd.DataFrame(st.session_state.materiales_totales)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MATERIALES_ESPECIFICACION')
    
    st.download_button(
        label="📥 DESCARGAR EXCEL CON MATERIALES (.xlsx)",
        data=output.getvalue(),
        file_name=f"Materiales_ECOLUZ_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    )
    
    if st.button("🔄 Iniciar nuevo proyecto"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
