import streamlit as st
import pandas as pd
import io
import datetime

# --- CONFIGURACIÓN DE DISEÑO ---
st.set_page_config(page_title="Cerebro ECOLUZ", layout="wide", page_icon="🧠")
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    h1 { color: #004d40; text-align: center; border-bottom: 4px solid #004d40; padding-bottom: 10px; }
    h2, h3 { color: #00695c; background-color: #e0f2f1; padding: 10px; border-radius: 8px; }
    .stButton>button { background-color: #004d40; color: white; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 CEREBRO ECOLUZ")
st.markdown("### *Especificaciones Técnicas y Materiales*")

# --- SIDEBAR ---
with st.sidebar:
    st.header("📎 Adjuntar Planos/Fotos")
    archivos_subidos = st.file_uploader("Sube archivos", accept_multiple_files=True)
    if archivos_subidos:
        st.success(f"✅ {len(archivos_subidos)} archivo(s) adjuntado(s).")

# --- MENÚ PRINCIPAL ---
especialidad = st.selectbox("SELECCIONA LA ESPECIALIDAD:", 
    ["Selecciona...", "Construcción Nueva", "Remodelación", "Reparación", "Electricidad", "Gasfitería", "Pintura", "Techumbre", "Jardinería", "Climatización"])

# Diccionario para guardar las respuestas
respuestas = {}

if especialidad != "Selecciona...":
    st.header(f"📋 CUESTIONARIO: {especialidad.upper()}")
    
    with st.form(f"form_{especialidad}"):
        
        # ===================== CONSTRUCCIÓN NUEVA =====================
        if especialidad == "Construcción Nueva":
            st.subheader("1. Información del Proyecto")
            c1, c2 = st.columns(2)
            with c1:
                respuestas['c_tipo'] = st.selectbox("¿Qué tipo de construcción?", ["Casa", "Local comercial", "Galpón", "Oficina", "Bodega"])
                respuestas['c_uso'] = st.text_input("¿Cuál será el uso principal?")
                respuestas['c_pisos'] = st.selectbox("¿Será de uno o más pisos?", ["1 Piso", "2 Pisos", "3 o más pisos"])
            with c2:
                respuestas['c_planos'] = st.radio("¿Cuenta con planos?", ["Sí, tengo planos", "Necesito diseño"])

            st.subheader("2. Terreno y Fundaciones")
            respuestas['t_ubicacion'] = st.text_input("Dirección del terreno")
            respuestas['t_terreno'] = st.selectbox("¿El terreno es plano o pendiente?", ["Plano", "Pendiente suave", "Pendiente pronunciada"])
            respuestas['t_servicios'] = st.radio("¿Cuenta con agua y electricidad?", ["Sí", "No"])
            respuestas['t_alcantarillado'] = st.radio("¿Alcantarillado o fosa séptica?", ["Alcantarillado público", "Fosa séptica"])
            respuestas['t_estudio'] = st.radio("¿Se realizó estudio de suelo?", ["Sí", "No"])

            st.subheader("3. Estructura, Muros y Materiales")
            respuestas['sys_const'] = st.selectbox("Sistema constructivo:", ["Albañilería", "Hormigón armado", "Metalcon", "Madera", "Panel SIP"])
            if respuestas['sys_const'] == "Albañilería":
                respuestas['ladrillo'] = st.selectbox("Tipo de ladrillo:", ["Ladrillo Fiscal", "Ladrillo Princesa"])
                respuestas['estuco_int'] = st.radio("¿Llevará estuco interior?", ["Sí", "No"])
                respuestas['estuco_ext'] = st.radio("¿Llevará estuco exterior?", ["Sí", "No"])
                if respuestas['estuco_ext'] == "Sí":
                    respuestas['impermeabilizante'] = st.radio("¿Llevará impermeabilizante en el estuco exterior?", ["Sí", "No"])
            elif respuestas['sys_const'] == "Metalcon":
                respuestas['metalcon_perfil'] = st.text_input("Espesor de perfiles (Ej: 90mm):")

            st.subheader("4. Techumbre y Pisos")
            respuestas['techo_tipo'] = st.selectbox("Tipo de cubierta:", ["Zinc", "Teja", "PV4", "Teja asfáltica"])
            respuestas['techo_aislacion'] = st.radio("¿Instalará aislación térmica?", ["Sí", "No"])
            respuestas['piso_tipo'] = st.selectbox("Tipo de piso:", ["Cerámica", "Porcelanato", "Flotante", "Vinílico", "Radier afinado"])
            
            st.subheader("5. Instalaciones Eléctricas y Sanitarias")
            respuestas['enchufes'] = st.number_input("N° de enchufes:", min_value=0)
            respuestas['luminarias'] = st.number_input("N° de luminarias:", min_value=0)
            respuestas['banos'] = st.number_input("N° de baños:", min_value=0)
            respuestas['cert_sec'] = st.radio("¿Necesita certificación SEC?", ["Sí", "No"])

            st.subheader("6. Presupuesto y Plazos")
            respuestas['presupuesto'] = st.number_input("Presupuesto disponible (CLP):", min_value=0)
            respuestas['inicio'] = st.text_input("Fecha estimada de inicio:")
            respuestas['plazo'] = st.text_input("Plazo estimado de entrega:")

        # ===================== REMODELACIÓN =====================
        elif especialidad == "Remodelación":
            st.subheader("1. Información General")
            respuestas['rm_area'] = st.text_input("¿Qué espacio desea remodelar? (Ej: Casa, local, oficina)")
            respuestas['rm_partes'] = st.text_input("¿Qué áreas se remodelarán? (Cocina, baño, living, fachada)")
            respuestas['rm_objetivo'] = st.text_area("¿Cuál es el objetivo de la remodelación?")
            respuestas['rm_habitada'] = st.radio("¿La propiedad está habitada durante la remodelación?", ["Sí", "No"])

            st.subheader("2. Estado Actual y Demolición")
            respuestas['rm_daños'] = st.text_area("¿Cuál es el problema principal? (Grietas, humedad, filtraciones)")
            respuestas['rm_demoler'] = st.radio("¿Se demolerán muros?", ["Sí", "No"])
            if respuestas['rm_demoler'] == "Sí":
                respuestas['rm_estructural'] = st.radio("¿Los muros a demoler son estructurales?", ["Sí", "No"])
            respuestas['rm_escombros'] = st.radio("¿Se necesita retiro de escombros?", ["Sí", "No"])

            st.subheader("3. Cambios y Materiales")
            respuestas['rm_piso'] = st.radio("¿Se cambiarán los pisos?", ["Sí", "No"])
            if respuestas['rm_piso'] == "Sí":
                respuestas['rm_piso_tipo'] = st.selectbox("Nuevo tipo de piso:", ["Cerámica", "Porcelanato", "Flotante", "Vinílico", "Madera"])
            respuestas['rm_puertas'] = st.radio("¿Se reemplazarán puertas y ventanas?", ["Sí", "No"])
            
            st.subheader("4. Presupuesto y Plazos")
            respuestas['rm_presupuesto'] = st.number_input("Presupuesto disponible:", min_value=0)
            respuestas['rm_inicio'] = st.text_input("Fecha estimada de inicio:")

        # ===================== REPARACIÓN =====================
        elif especialidad == "Reparación":
            st.subheader("1. Información General")
            respuestas['rep_que'] = st.text_area("¿Qué necesita reparar y dónde se encuentra?")
            respuestas['rep_desde'] = st.text_input("¿Desde cuándo presenta la falla?")
            respuestas['rep_causa'] = st.text_input("¿Cuál cree que fue la causa del problema?")
            respuestas['rep_urgente'] = st.radio("¿La reparación es urgente?", ["Sí", "No"])

            st.subheader("2. Evaluación del Daño")
            respuestas['rep_estructura'] = st.radio("¿El problema afecta la estructura?", ["Sí", "No", "No sé"])
            respuestas['rep_empeora'] = st.radio("¿El daño continúa empeorando?", ["Sí", "No", "No sé"])
            
            st.subheader("3. Detalles del Daño")
            respuestas['rep_tipo'] = st.selectbox("¿Qué tipo de daño es?", ["Grietas/Fisuras", "Humedad/Filtraciones", "Desprendimiento de estuco", "Problema eléctrico", "Fuga de agua", "Otro"])
            respuestas['rep_material'] = st.selectbox("Material del elemento dañado:", ["Ladrillo", "Bloque", "Hormigón", "Metalcon", "Madera", "Otro"])

            st.subheader("4. Presupuesto y Ejecución")
            respuestas['rep_presupuesto'] = st.number_input("Presupuesto disponible:", min_value=0)
            respuestas['rep_inicio'] = st.text_input("¿Cuándo necesita realizar la reparación?")

        # ===================== BOTÓN DE ENVIAR =====================
        enviar = st.form_submit_button("🛠️ GENERAR ESPECIFICACIÓN Y EXCEL DE MATERIALES")

    # ===================== LÓGICA DE CÁLCULO Y EXCEL =====================
    if enviar:
        st.success("✅ ¡Especificación guardada! Calculando materiales...")
        lista_materiales = []
        
        # Lógica de Materiales para Construcción Nueva
        if especialidad == "Construcción Nueva":
            # Simulación de cálculo basada en respuestas
            lista_materiales.append(["Fundaciones", "Cemento", "10 sacos"])
            lista_materiales.append(["Fundaciones", "Arena", "5 m3"])
            
            if respuestas['sys_const'] == "Albañilería":
                lista_materiales.append(["Muros", "Ladrillos", "600 unid"])
                if respuestas['estuco_int'] == "Sí":
                    lista_materiales.append(["Estuco Interior", "Cemento", "8 sacos"])
                    lista_materiales.append(["Estuco Interior", "Arena", "4 m3"])
                if respuestas['estuco_ext'] == "Sí":
                    lista_materiales.append(["Estuco Exterior", "Cemento", "10 sacos"])
                    lista_materiales.append(["Estuco Exterior", "Arena", "5 m3"])
                    if respuestas['impermeabilizante'] == "Sí":
                        lista_materiales.append(["Impermeabilizante", "Sellador", "2 unid"])
            elif respuestas['sys_const'] == "Metalcon":
                lista_materiales.append(["Estructura", "Perfiles Metalcon", "40 unid"])
                
        # Lógica de Materiales para Remodelación
        elif especialidad == "Remodelación":
            if respuestas['rm_demoler'] == "Sí":
                lista_materiales.append(["Demolición", "Retiro escombros", "1 m3"])
            if respuestas['rm_piso'] == "Sí":
                lista_materiales.append(["Pisos", respuestas['rm_piso_tipo'], "10 m2"])
                
        # Lógica de Materiales para Reparación
        elif especialidad == "Reparación":
            if "Humedad" in respuestas['rep_tipo']:
                lista_materiales.append(["Reparación", "Impermeabilizante", "1 unid"])
            lista_materiales.append(["Reparación", "Pasta muro", "2 bolsas"])
            lista_materiales.append(["Reparación", "Pintura", "1 galón"])

        # Crear DataFrame y descargar
        df = pd.DataFrame(lista_materiales, columns=["Partida", "Material", "Cantidad"])
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MATERIALES_CEREBRO')
        
        st.download_button(
            label="📥 DESCARGAR EXCEL CON MATERIALES",
            data=output.getvalue(),
            file_name=f"Materiales_{especialidad}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.info("💡 Instrucción: Abre tu archivo 'ECOLUZ_v3.0_RC6.xlsx', ve a 'DESGLOSE MATERIALES', y pega los datos de este archivo descargado para que el APU se calcule solo.")
