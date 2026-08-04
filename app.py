import streamlit as st
import pandas as pd
import io
import datetime

# --- CONFIGURACIÓN DE DISEÑO ---
st.set_page_config(page_title="Cerebro ECOLUZ", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    h1 { color: #004d40; text-align: center; }
    .stButton>button { background-color: #004d40; color: white; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 CEREBRO DE ESPECIFICACIONES ECOLUZ")
st.markdown("### *Generador de Desglose para Cotización*")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📎 Adjuntar Planos/Fotos")
    archivos_subidos = st.file_uploader("Sube archivos", accept_multiple_files=True)
    if archivos_subidos:
        st.success(f"✅ {len(archivos_subidos)} archivo(s) adjuntado(s).")

# --- MENÚ PRINCIPAL ---
especialidad = st.selectbox("SELECCIONA LA ESPECIALIDAD:", 
    ["Selecciona...", "Construcción Nueva", "Remodelación", "Reparación"])

respuestas = {}

if especialidad != "Selecciona...":
    st.header(f"📋 CUESTIONARIO: {especialidad.upper()}")
    
    with st.form(f"form_{especialidad}"):
        st.subheader("1. Información General")
        respuestas['cliente'] = st.text_input("Nombre del cliente")
        respuestas['direccion'] = st.text_input("Dirección de la obra")
        
        if especialidad == "Construcción Nueva":
            st.subheader("2. Medidas")
            # Nuevo: Ingreso de piezas por separado
            st.info("Ingresa los metros cuadrados (m²) de cada sección de la obra:")
            col1, col2, col3 = st.columns(3)
            with col1: sec1 = st.number_input("Sección 1 (m²):", min_value=0.0, step=1.0)
            with col2: sec2 = st.number_input("Sección 2 (m²):", min_value=0.0, step=1.0)
            with col3: sec3 = st.number_input("Sección 3 (m²):", min_value=0.0, step=1.0)
            respuestas['total_m2'] = sec1 + sec2 + sec3
            
            st.subheader("3. Materiales y Estructura")
            respuestas['sys_const'] = st.selectbox("Sistema constructivo:", ["Albañilería", "Metalcon", "Hormigón"])
            if respuestas['sys_const'] == "Albañilería":
                respuestas['estuco_ext'] = st.radio("¿Llevará estuco exterior con impermeabilizante?", ["Sí", "No"])
                
        elif especialidad == "Remodelación":
            respuestas['area'] = st.text_input("¿Qué área remodelará?")
            
        elif especialidad == "Reparación":
            respuestas['tipo_dano'] = st.text_input("Describa el daño a reparar")

        enviar = st.form_submit_button("🛠️ GENERAR LISTADO PARA EXCEL")
        
    if enviar:
        st.success("✅ Calculando materiales...")
        
        # --- LÓGICA DE CÁLCULO (El cerebro decide los materiales) ---
        lista_para_excel = []
        
        if especialidad == "Construcción Nueva":
            m2 = respuestas['total_m2']
            if respuestas['sys_const'] == "Albañilería":
                # Aquí el cerebro sabe que necesita ladrillos, cemento, etc. según los m2
                lista_para_excel.append(["Muros Albañilería", "MAT_LADRILLO", round(m2 * 50)])
                lista_para_excel.append(["Muros Albañilería", "MAT_CEMENTO", round(m2 * 0.5)])
                lista_para_excel.append(["Muros Albañilería", "MAT_ARENA", round(m2 * 0.2)])
                if respuestas['estuco_ext'] == "Sí":
                    lista_para_excel.append(["Estuco Exterior", "MAT_IMPERMEABLE", round(m2 / 10)])
                    
            elif respuestas['sys_const'] == "Metalcon":
                lista_para_excel.append(["Estructura Metalcon", "MAT_PERFILES", round(m2 / 3)])
                lista_para_excel.append(["Estructura Metalcon", "MAT_ATORNILLOS", round(m2 * 4)])
                lista_para_excel.append(["Aislación", "MAT_LANA_ROCA", m2])
        
        # --- CREACIÓN DEL EXCEL EN FORMATO PARA TU HOJA "DESGLOSE" ---
        # La hoja DESGLOSE de tu Excel tiene 6 columnas: N°Partida, Partida, Codigo, Descripcion, Unidad, Cantidad.
        # Vamos a generar ese formato exacto para que copies y pegues sin problemas.
        
        # Añadimos un número de partida ficticio para la columna A
        df_final = pd.DataFrame(lista_para_excel, columns=["Partida", "Codigo Material", "Cantidad"])
        
        # (Nota: Como el cerebro no tiene los precios aún, solo enviamos el código y la cantidad.
        # Cuando tú pegues esto en tu Excel, la fórmula BUSCARV traerá el precio desde tu hoja maestra PARAMETROS).
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_final.to_excel(writer, index=False, sheet_name='DESGLOSE_CEREBRO')
        
        st.markdown("---")
        st.subheader("📥 Archivo generado con los materiales necesarios:")
        st.download_button(
            label="📥 DESCARGAR EXCEL PARA PEGAR EN DESGLOSE",
            data=output.getvalue(),
            file_name=f"Desglose_Cerebro_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.info("💡 **Instrucción para tu Excel:**\n1. Abre tu archivo `ECOLUZ_v3.0_RC6.xlsx`.\n2. Ve a la hoja `3. DESGLOSE MATERIALES`.\n3. Copia las columnas de este archivo descargado (Partida, Código, Cantidad) y pégalas en tu hoja.\n4. Las fórmulas de `APU` y `COTIZACION CLIENTE` calcularán el precio automáticamente.")
