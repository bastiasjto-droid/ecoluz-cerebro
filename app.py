import streamlit as st
import pandas as pd
import io
import datetime

st.set_page_config(page_title="Cerebro ECOLUZ", layout="wide")
st.title("🧠 Cerebro de Especificaciones Técnicas ECOLUZ")

# --- SUBIDA DE ARCHIVOS ---
st.sidebar.header("📎 Adjuntar Archivos (Planos/Fotos)")
archivos_subidos = st.sidebar.file_uploader("Sube archivos para la especificación", accept_multiple_files=True)
if archivos_subidos:
    st.sidebar.success(f"✅ {len(archivos_subidos)} archivo(s) adjuntado(s).")

# --- LOGICA DE MATERIALES (Base de datos de prueba) ---
# Esto se conectará después a tu lista de precios real.
BASE_MATERIALES = {
    "MAT01": {"desc": "Plancha Simplisima 6mm 1,2x2,4m", "unidad": "unid"},
    "MAT02": {"desc": "Lana de roca 50mm 40-60kg/m3", "unidad": "m2"},
    "MAT03": {"desc": "Pino seco cepillado 1x2 3,2m", "unidad": "unid"},
    "MAT04": {"desc": "Sellador poliuretano Rex 600ml", "unidad": "unid"},
    "MAT05": {"desc": "Tornillos autoperforantes c/trompeta c/100", "unidad": "caja"},
    "MAT10": {"desc": "Ventana corredera aluminio 60x80cm", "unidad": "unid"},
    "MAT12": {"desc": "Ceramico blanco", "unidad": "m2"},
    "MAT16": {"desc": "Bolsas/productos limpieza", "unidad": "global"},
}

# --- MENÚ PRINCIPAL ---
especialidad = st.selectbox("Selecciona la especialidad del trabajo:", 
    ["Selecciona...", "Construcción Nueva", "Remodelación", "Reparación", "Electricidad", "Gasfitería", "Pintura", "Techumbre", "Jardinería", "Climatización"])

# Diccionario para guardar las respuestas
respuestas = {}

if especialidad != "Selecciona...":
    st.header(f"📋 Cuestionario Dinámico para: {especialidad}")
    
    with st.form(f"form_{especialidad}"):
        
        st.subheader("1. Información General")
        respuestas['cliente'] = st.text_input("Nombre del cliente")
        respuestas['direccion'] = st.text_input("Dirección exacta de la obra")
        respuestas['m2'] = st.number_input("Metros cuadrados (m²) aproximados del proyecto:", min_value=1.0, step=1.0)
        
        st.divider()

        # Lógica para guardar respuestas según especialidad
        if especialidad == "Construcción Nueva":
            st.subheader("2. Estructura")
            tipo = st.selectbox("Tipo de construcción:", ["Albañilería", "Hormigón", "Metalcon"], key="c_tipo")
            respuestas['tipo'] = tipo
            
        elif especialidad == "Electricidad":
            st.subheader("2. Instalación Eléctrica")
            respuestas['circuitos'] = st.number_input("¿Cuántos circuitos independientes?", min_value=1, key="e_circuitos")
            respuestas['enchufes'] = st.number_input("¿Cuántos enchufes?", min_value=0, key="e_enchufes")
            respuestas['luminarias'] = st.number_input("¿Cuántas luminarias?", min_value=0, key="e_luminarias")
            
        # (Aquí podrías agregar más lógica para las otras especialidades según crezca)

        enviar = st.form_submit_button("🛠️ GENERAR ESPECIFICACIÓN Y EXCEL")

    # --- GENERACIÓN DEL EXCEL ---
    if enviar:
        st.success("✅ ¡Especificación generada! Generando archivo Excel para tu cotización...")
        
        # 1. SIMULACIÓN DE CÁLCULOS (Aquí el cerebro decide qué materiales poner)
        lista_materiales_excel = []
        
        # Ejemplo de lógica que el cerebro usará en el futuro:
        if especialidad == "Construcción Nueva":
            # Calcular materiales según m2
            m2 = respuestas['m2']
            lista_materiales_excel.append(["Empalizado", "MAT03", m2]) # Simulación
            lista_materiales_excel.append(["Empalizado", "MAT05", 2]) 
            lista_materiales_excel.append(["Revestimiento", "MAT01", round(m2/2)])
            
        elif especialidad == "Electricidad":
            lista_materiales_excel.append(["Instalación Eléctrica", "MAT04", respuestas['enchufes'] * 2])
            lista_materiales_excel.append(["Iluminación", "MAT05", respuestas['luminarias']])

        # 2. CREAR EL DATAFRAME DE EXCEL (Con el formato exacto de tu hoja DESGLOSE)
        df_output = pd.DataFrame(lista_materiales_excel, columns=["Partida", "Codigo Material", "Cantidad"])
        
        # 3. CONVERTIR A EXCEL PARA DESCARGA
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_output.to_excel(writer, index=False, sheet_name='DESGLOSE_MATERIALES')
        
        processed_data = output.getvalue()
        
        # 4. BOTÓN DE DESCARGA
        st.download_button(
            label="📥 DESCARGAR EXCEL PARA COTIZACIÓN",
            data=processed_data,
            file_name=f"Materiales_Cerebro_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.write("💡 **Instrucción:** Abre tu archivo `ECOLUZ_v3.0_RC6.xlsx`. Ve a la hoja `3. DESGLOSE MATERIALES`. Copi
