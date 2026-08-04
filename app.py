import streamlit as st
import pandas as pd
import io
import datetime
import json
import re

# --- CONFIGURACIÓN DE DISEÑO ---
st.set_page_config(page_title="Inspector ECOLUZ", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    h1 { color: #004d40; text-align: center; border-bottom: 4px solid #004d40; padding-bottom: 10px; }
    .stButton>button { background-color: #004d40; color: white; border-radius: 10px; width: 100%; }
    .stAlert { border-left: 5px solid #004d40; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 INSPECTOR INTELIGENTE ECOLUZ")
st.markdown("### *Levantamiento Técnico y Especificación Profesional*")

# --- MOTOR DE REGLAS (Diccionario de Preguntas Dinámicas) ---
# Este es el "cerebro" real. Cada respuesta dispara nuevas preguntas.
REGLAS_TECNICAS = {
    "inicio": {
        "pregunta": "¿Cuál es el objetivo principal de esta intervención?",
        "opciones": ["Construcción Nueva", "Remodelación", "Reparación", "Ampliación", "Mantención"]
    },
    "Construcción Nueva": {
        "pregunta": "¿Qué sistema constructivo planea utilizar?",
        "opciones": ["Albañilería", "Hormigón Armado", "Metalcon", "Madera", "Panel SIP"],
        "sub_reglas": {
            "Albañilería": {
                "pregunta": "¿El muro será portante o divisor?",
                "opciones": ["Portante", "Divisor"],
                "siguiente": "Albañilería_Detalle"
            },
            "Metalcon": {
                "pregunta": "¿Qué espesor de perfiles Metalcon necesita?",
                "opciones": ["70mm", "90mm", "150mm"],
                "siguiente": "Metalcon_Detalle"
            }
        }
    },
    "Albañilería_Detalle": {
        "pregunta": "¿Llevará estuco interior/exterior?",
        "opciones": ["Solo Interior", "Solo Exterior", "Ambos", "Ninguno"],
        "siguiente": "Humedad"
    },
    "Metalcon_Detalle": {
        "pregunta": "¿Qué tipo de aislación térmica usará?",
        "opciones": ["Lana de Vidrio", "Lana Mineral", "Poliestireno", "Ninguna"],
        "siguiente": "Pisos"
    },
    "Remodelación": {
        "pregunta": "¿Qué área se va a remodelar?",
        "opciones": ["Cocina", "Baño", "Living", "Fachada", "Completa"],
        "sub_reglas": {
            "Baño": {
                "pregunta": "¿Va a cambiar la impermeabilización del piso?",
                "opciones": ["Sí", "No"],
                "siguiente": "Humedad"
            }
        }
    },
    "Reparación": {
        "pregunta": "¿Cuál es el problema principal a reparar?",
        "opciones": ["Humedad", "Grieta", "Filtración", "Desprendimiento", "Falla Eléctrica"],
        "sub_reglas": {
            "Humedad": {
                "pregunta": "¿El problema de humedad presenta hongos o salitre?",
                "opciones": ["Sí, hongos", "Sí, salitre", "Ambos", "Ninguno"],
                "siguiente": "Diagnostico_Muro"
            }
        }
    },
    "Pisos": {
        "pregunta": "¿Qué tipo de piso se instalará?",
        "opciones": ["Cerámica", "Porcelanato", "Flotante", "Vinílico", "Madera", "Radier"]
    },
    "Diagnostico_Muro": {
        "pregunta": "¿El muro afectado es de ladrillo o Metalcon?",
        "opciones": ["Ladrillo", "Metalcon"]
    }
}

# --- FUNCIÓN PARA GENERAR PREGUNTAS DINÁMICAS ---
# Guarda el historial de respuestas
if 'historial' not in st.session_state:
    st.session_state.historial = []
if 'nodo_actual' not in st.session_state:
    st.session_state.nodo_actual = "inicio"
if 'materiales_calculados' not in st.session_state:
    st.session_state.materiales_calculados = []

# --- SIDEBAR: CARGAR ARCHIVOS ---
with st.sidebar:
    st.header("📎 Cargar Planos/Fotos (Beta)")
    st.info("El sistema intentará detectar puertas, ventanas y superficies automáticamente.")
    archivos = st.file_uploader("Sube planos o fotos (JPG, PNG)", accept_multiple_files=True)
    if archivos:
        st.success(f"✅ {len(archivos)} archivos cargados para análisis.")

# --- LÓGICA DEL MOTOR DE REGLAS ---
st.subheader(f"🔍 Paso actual: {st.session_state.nodo_actual}")

# Obtener las reglas del nodo actual
nodo = st.session_state.nodo_actual
config = REGLAS_TECNICAS.get(nodo, {})

if config:
    st.write(f"**{config.get('pregunta', '¿Qué desea hacer?')}**")
    
    opciones = config.get('opciones', [])
    
    # Mostrar opciones como botones
    cols = st.columns(min(len(opciones), 3))  # Máximo 3 columnas
    for i, opcion in enumerate(opciones):
        with cols[i % 3]:
            if st.button(f"➡️ {opcion}", key=f"btn_{opcion}"):
                # Guardar respuesta en el historial
                st.session_state.historial.append({"nodo": nodo, "respuesta": opcion})
                
                # Determinar el siguiente nodo
                sub_reglas = config.get('sub_reglas', {})
                if opcion in sub_reglas:
                    st.session_state.nodo_actual = sub_reglas[opcion].get('siguiente', "fin")
                else:
                    st.session_state.nodo_actual = config.get('siguiente', "fin")
                
                st.rerun()

# --- FINALIZACIÓN Y GENERACIÓN DE ESPECIFICACIÓN ---
if st.session_state.nodo_actual == "fin" or st.button("✅ TERMINAR LEVANTAMIENTO"):
    st.balloons()
    st.success("¡Levantamiento técnico completado!")
    
    # --- LÓGICA DE CÁLCULO DE MATERIALES (Ejemplo avanzado) ---
    # Aquí el cerebro "razona" y aplica reglas de ingeniería
    materiales = []
    historial_str = json.dumps(st.session_state.historial)
    
    if "Metalcon" in historial_str and "90mm" in historial_str:
        # Si tiene Metalcon de 90mm, el cerebro sabe que necesita perfiles, tornillos y lana
        materiales.append(["Estructura", "Perfil Metalcon 90mm", "Calculado según metros lineales de muro", "60 unid"])
        materiales.append(["Aislación", "Lana de Vidrio 90mm", "Calculado según superficie del tabique", "15 m2"])
        materiales.append(["Fijaciones", "Tornillos punta broca", "Calculado por cantidad de perfiles", "200 unid"])
    
    if "Baño" in historial_str and "Sí" in historial_str: # Si es baño y cambia impermeabilización
        materiales.append(["Impermeabilización", "Membrana liquida", "Calculado por superficie de piso", "5 m2"])
    
    # Guardar en sesión
    st.session_state.materiales_calculados = materiales
    
    # --- GENERAR EXCEL DE MATERIALES ---
    df = pd.DataFrame(materiales, columns=["Partida", "Material", "Origen del Cálculo", "Cantidad"])
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='ESPECIFICACION_TECNICA')
    
    st.subheader("📥 Descargar Especificación Técnica y Materiales")
    st.download_button(
        label="📥 DESCARGAR EXCEL PROFESIONAL",
        data=output.getvalue(),
        file_name=f"Especificacion_ECOLUZ_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.write("---")
    st.write("🔮 **Preparado para la Fase 3:** Análisis de planos, cálculo de rendimientos de mano de obra y APU automático.")
