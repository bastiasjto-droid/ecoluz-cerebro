import streamlit as st
import pandas as pd
import io
import datetime
import json

# --- CONFIGURACIÓN DE DISEÑO ---
st.set_page_config(page_title="Inspector ECOLUZ", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    h1 { color: #004d40; text-align: center; border-bottom: 4px solid #004d40; padding-bottom: 10px; }
    .stButton>button { background-color: #004d40; color: white; border-radius: 10px; width: 100%; }
    .stProgress > div > div > div > div { background-color: #004d40; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 INSPECTOR INTELIGENTE ECOLUZ")
st.markdown("### *Levantamiento Técnico Guiado Paso a Paso*")

# --- ESTADO DE LA SESIÓN (Memoria del Cerebro) ---
if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = 0
if 'historial' not in st.session_state:
    st.session_state.historial = []
if 'ruta_completa' not in st.session_state:
    st.session_state.ruta_completa = []

# --- CONFIGURACIÓN DEL FLUJO (Árbol de Navegación) ---
FLUJO_TECNICO = {
    0: {
        "titulo": "Paso 1 de 5: ¿Qué desea realizar hoy?",
        "pregunta": "Seleccione el tipo de servicio a cotizar:",
        "opciones": ["Construcción Nueva", "Remodelación", "Reparación", "Mantención", "Ampliación"],
        "siguiente_paso": 1
    },
    1: {
        "titulo": "Paso 2 de 5: Especialidad requerida",
        "pregunta": "¿Qué especialidad técnica involucra este proyecto?",
        "opciones": ["Construcción (Albañilería/Metalcon)", "Pintura y Estucos", "Electricidad y SEC", "Gasfitería y Sanitarios", "Carpintería y Molduras", "Revestimientos y Pisos"],
        "siguiente_paso": 2
    },
    2: {
        "titulo": "Paso 3 de 5: Área de intervención",
        "pregunta": "¿Qué recinto o área específica se va a intervenir?",
        "opciones": ["Cocina", "Baño", "Living/Comedor", "Habitaciones", "Fachada Exterior", "Toda la propiedad"],
        "siguiente_paso": 3
    },
    3: {
        "titulo": "Paso 4 de 5: Estado y Diagnóstico",
        "pregunta": "¿Cuál es el estado actual o el problema principal en esa área?",
        "opciones": ["Buen estado (solo mejoras)", "Humedad / Filtraciones", "Grietas / Daños estructurales", "Desgaste por uso", "Instalaciones obsoletas"],
        "siguiente_paso": 4
    },
    4: {
        "titulo": "Paso 5 de 5: Materiales y Preferencias",
        "pregunta": "¿Con qué tipo de calidad de materiales desea trabajar?",
        "opciones": ["Económico", "Estándar", "Premium"],
        "siguiente_paso": -1  # -1 significa "Fin del levantamiento"
    }
}

# --- BARRA DE PROGRESO ---
progress_val = (st.session_state.paso_actual + 1) / len(FLUJO_TECNICO)
st.progress(progress_val)

# --- VARIABLE PARA CONTROLAR EL FIN ---
levantamiento_terminado = False

# --- LÓGICA DE NAVEGACIÓN ---
paso_actual = st.session_state.paso_actual

# Si el paso actual es -1, el levantamiento terminó
if paso_actual == -1:
    levantamiento_terminado = True

# Si el levantamiento NO ha terminado, mostramos la pregunta actual
if not levantamiento_terminado:
    config = FLUJO_TECNICO.get(paso_actual)
    
    if config:
        st.subheader(config["titulo"])
        st.write(f"**{config['pregunta']}**")
        
        opciones = config['opciones']
        siguiente = config['siguiente_paso']
        
        st.write("---")
        # Mostramos los botones (máximo 3 por fila para que se vea bien en celular)
        cols = st.columns(min(len(opciones), 3))
        
        for i, opcion in enumerate(opciones):
            with cols[i % 3]:
                if st.button(f"➡️ {opcion}", key=f"btn_{paso_actual}_{i}"):
                    # 1. Guardar respuesta en el historial
                    st.session_state.historial.append({"paso": paso_actual, "respuesta": opcion})
                    # 2. Guardar la ruta para la especificación
                    st.session_state.ruta_completa.append(opcion)
                    # 3. Actualizar el paso actual al siguiente
                    st.session_state.paso_actual = siguiente
                    # 4. Recargar la página para mostrar el nuevo paso
                    st.rerun()

# --- PANTALLA FINAL (Generación del Informe) ---
if levantamiento_terminado:
    st.balloons()
    st.success("🎯 ¡Levantamiento técnico completado exitosamente!")
    
    st.markdown("---")
    st.subheader("📋 Resumen del levantamiento realizado:")
    for i, respuesta in enumerate(st.session_state.ruta_completa):
        st.write(f"**Paso {i+1}:** {respuesta}")
    
    st.markdown("---")
    st.subheader("🛠️ ESPECIFICACIÓN TÉCNICA Y MATERIALES")
    
    # --- Lógica Inteligente de Materiales basada en las respuestas ---
    lista_materiales = []
    
    # Analizamos el historial para saber qué materiales calcular
    if "Construcción Nueva" in st.session_state.ruta_completa:
        lista_materiales.append(["Cimientos", "Cemento", "10 sacos"])
        lista_materiales.append(["Cimientos", "Arena", "5 m3"])
        
        if "Metalcon" in st.session_state.ruta_completa: # El sistema debe detectar Metalcon
            lista_materiales.append(["Estructura", "Perfiles Metalcon", "40 unid"])
            lista_materiales.append(["Aislación", "Lana de Vidrio", "15 m2"])
            lista_materiales.append(["Fijaciones", "Tornillos autoperforantes", "2 cajas"])
            
        elif "Albañilería" in st.session_state.ruta_completa:
            lista_materiales.append(["Muros", "Ladrillos", "600 unid"])
            
    if "Humedad" in st.session_state.ruta_completa:
        lista_materiales.append(["Reparación", "Impermeabilizante", "2 unid"])
        lista_materiales.append(["Reparación", "Sellador de grietas", "1 unid"])
        
    if "Premium" in st.session_state.ruta_completa:
        lista_materiales.append(["Terminaciones", "Pintura Premium", "2 galones"])
        
    # Convertir a DataFrame y descargar
    df = pd.DataFrame(lista_materiales, columns=["Partida", "Material", "Cantidad"])
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='ESPECIFICACION_TECNICA')
    
    st.download_button(
        label="📥 DESCARGAR ESPECIFICACIÓN Y MATERIALES (.xlsx)",
        data=output.getvalue(),
        file_name=f"Especificacion_ECOLUZ_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # Botón para reiniciar el proceso
    if st.button("🔄 Iniciar nuevo levantamiento"):
        st.session_state.paso_actual = 0
        st.session_state.historial = []
        st.session_state.ruta_completa = []
        st.rerun()
