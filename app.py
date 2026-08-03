
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cerebro ECOLUZ", layout="wide")
st.title("🧠 Cerebro de Especificaciones Técnicas")

# --- SUBIDA DE ARCHIVOS (Siempre visible) ---
st.sidebar.header("📎 Adjuntar Archivos")
st.sidebar.write("Sube planos, fotos o documentos para la especificación:")
archivos_subidos = st.sidebar.file_uploader("Selecciona archivos", accept_multiple_files=True)
if archivos_subidos:
    st.sidebar.success(f"✅ {len(archivos_subidos)} archivo(s) adjuntado(s).")

# --- OPCIONES DINÁMICAS ---
especialidad = st.selectbox("Selecciona la especialidad del trabajo:", 
    ["Selecciona...", "Construcción Nueva", "Remodelación", "Reparación", "Mantención", "Electricidad", "Gasfitería", "Pintura", "Techumbre", "Jardinería / Paisajismo", "Climatización"])

if especialidad != "Selecciona...":
    st.header(f"📋 Cuestionario Dinámico para: {especialidad}")
    
    with st.form(f"form_{especialidad}"):
        
        # --- PREGUNTAS COMUNES PARA TODOS ---
        st.subheader("1. Información General del Cliente")
        nombre_cliente = st.text_input("Nombre del cliente")
        rut_cliente = st.text_input("RUT del cliente (si aplica)")
        direccion_obra = st.text_input("Dirección exacta de la obra")
        telefono_contacto = st.text_input("Teléfono de contacto")
        correo_contacto = st.text_input("Correo electrónico")

        st.divider()

        # --- PREGUNTAS SEGÚN LA ESPECIALIDAD ELEGIDA ---
        
        if especialidad == "Construcción Nueva":
            st.subheader("2. Terreno y Cimientos")
            st.radio("¿El terreno está limpio?", ["Sí", "No"], key="c_limpio")
            st.selectbox("Tipo de terreno:", ["Plano", "Pendiente suave", "Pendiente pronunciada"], key="c_terreno")
            st.radio("¿Hay acceso para maquinaria?", ["Sí", "No"], key="c_maquinaria")
            st.radio("¿Cuenta con agua y electricidad?", ["Sí", "No"], key="c_servicios")
            st.selectbox("¿Qué tipo de fundación desea?", ["Corrida", "Aislada", "Losa de fundación"], key="c_fundacion")
            
            st.subheader("3. Materiales y Estructura")
            tipo_constructivo = st.selectbox("Tipo de construcción:", ["Albañilería", "Hormigón", "Metalcon", "Madera", "Panel SIP"], key="c_tipo")
            if tipo_constructivo == "Albañilería":
                st.selectbox("Tipo de ladrillo:", ["Ladrillo Fiscal", "Ladrillo Princesa"], key="c_ladrillo")
                st.radio("Llevará estuco interior", ["Sí", "No"], key="c_estuco_int")
                st.radio("Llevará estuco exterior", ["Sí", "No"], key="c_estuco_ext")
            elif tipo_constructivo == "Metalcon":
                st.text_input("Espesor de perfiles (Ej: 90mm):", key="c_perfiles")
                st.radio("Llevará aislación térmica", ["Sí", "No"], key="c_aislacion_mc")

            st.subheader("4. Techumbre y Terminaciones")
            st.selectbox("Tipo de techo:", ["Zinc", "Teja", "PV4", "Teja Asfáltica"], key="c_techo")
            st.radio("Llevará canaletas", ["Sí", "No"], key="c_canaletas")
            st.selectbox("Tipo de piso:", ["Cerámica", "Porcelanato", "Flotante", "Vinílico", "Radier"], key="c_piso")
            st.selectbox("Tipo de ventanas:", ["Aluminio", "PVC"], key="c_ventanas")

        elif especialidad == "Remodelación":
            st.subheader("2. Diagnóstico de la Remodelación")
            st.selectbox("¿Qué parte desea remodelar?", ["Cocina", "Baño", "Living/Comedor", "Habitaciones", "Exterior", "Todo el inmueble"], key="r_zona")
            st.radio("¿Se demolerán muros?", ["Sí", "No"], key="r_demolicion")
            st.radio("¿Los muros a demoler son estructurales?", ["Sí", "No", "No sé"], key="r_estructural")
            st.radio("¿Se cambiará el piso?", ["Sí", "No"], key="r_piso")
            st.radio("¿Se cambiarán puertas y ventanas?", ["Sí", "No"], key="r_puertas")
            st.radio("¿Se reutilizarán materiales existentes?", ["Sí", "No"], key="r_reutilizar")

        elif especialidad == "Reparación":
            st.subheader("2. Diagnóstico del Daño")
            st.text_area("Describa el problema o daño a reparar:", key="rep_descripcion")
            st.selectbox("¿Desde cuándo ocurre?", ["Hace menos de 1 semana", "Hace 1 mes", "Hace más de 6 meses"], key="rep_tiempo")
            st.radio("¿Ya fue reparado anteriormente?", ["Sí", "No"], key="rep_reparado")
            st.radio("¿Existe humedad o filtraciones?", ["Sí", "No"], key="rep_humedad")
            st.radio("¿El daño afecta la estructura?", ["Sí", "No"], key="rep_estructura")

        elif especialidad == "Electricidad":
            st.subheader("2. Especificación Eléctrica")
            st.selectbox("¿Cuál es el voltaje del proyecto?", ["110V", "220V", "380V", "Trifásica"], key="e_voltaje")
            st.number_input("¿Cuántos circuitos independientes necesita?", min_value=1, key="e_circuitos")
            st.number_input("¿Cuántos enchufes totales?", min_value=0, key="e_enchufes")
            st.number_input("¿Cuántas luminarias?", min_value=0, key="e_luminarias")
            st.radio("¿Habrá generador de respaldo?", ["Sí", "No"], key="e_generador")
            st.radio("¿Necesita sistema de puesta a tierra?", ["Sí", "No"], key="e_tierra")
            st.radio("¿Se solicitará aumento de potencia a la compañía?", ["Sí", "No"], key="e_potencia")

        elif especialidad == "Gasfitería":
            st.subheader("2. Especificación de Gasfitería")
            st.radio("¿Instalación de agua nueva o modificación?", ["Instalación nueva", "Modificación existente"], key="g_agua_tipo")
            st.radio("¿Requiere agua caliente?", ["Sí", "No"], key="g_agua_caliente")
            st.text_input("Tipo de calefón o termo a instalar:", key="g_calefon")
            st.radio("¿Hay conexión a alcantarillado o fosa séptica?", ["Alcantarillado público", "Fosa séptica"], key="g_alcantarillado")
            st.number_input("Número de baños a instalar/arreglar:", min_value=0, key="g_banos")
            st.selectbox("Tipo de grifería:", ["Económica", "Estándar", "Premium"], key="g_griferia")

        elif especialidad == "Pintura":
            st.subheader("2. Especificación de Pintura")
            st.number_input("Metros cuadrados (m²) aproximados a pintar:", min_value=1.0, key="p_m2")
            st.selectbox("Tipo de superficie a pintar:", ["Muros interiores", "Muros exteriores", "Madera", "Metales"], key="p_superficie")
            st.radio("¿Aplicará pintura antihumedad?", ["Sí", "No"], key="p_humedad")
            st.radio("¿Se requiere lijado y preparación de superficies?", ["Sí", "No"], key="p_lijado")
            st.selectbox("Calidad de la pintura deseada:", ["Económica", "Estándar", "Premium"], key="p_calidad")
            st.text_input("Colores o tonos a utilizar:", key="p_colores")

        elif especialidad == "Techumbre":
            st.subheader("2. Especificación de Techumbre")
            st.selectbox("Tipo de material de cubierta:", ["Plancha Zinc", "Teja de Arcilla", "Teja Asfáltica", "Policarbonato", "PV4"], key="t_material")
            st.number_input("Superficie total del techo (m²):", min_value=1.0, key="t_m2")
            st.radio("¿Llevará aislación térmica en el techo?", ["Sí", "No"], key="t_aislacion")
            st.text_input("Tipo de aislación y espesor (Ej: Lana de vidrio 50mm):", key="t_aislacion_tipo")
            st.radio("¿Incluye canaletas y bajadas de agua?", ["Sí", "No"], key="t_canaletas")
            st.radio("¿Llevará cielo falso (cielo raso)?", ["Sí", "No"], key="t_cielo")

        elif especialidad == "Jardinería / Paisajismo":
            st.subheader("2. Especificación de Paisajismo")
            st.number_input("Superficie total del jardín (m²):", min_value=1.0, key="j_m2")
            st.selectbox("Tipo de suelo actual:", ["Tierra natural", "Tierra de hoja", "Pastos", "Piedras", "Tierra con césped"], key="j_suelo")
            st.radio("¿Quiere sistema de riego automático?", ["Sí", "No"], key="j_riego")
            st.text_area("Tipo de especies de plantas o árboles a incluir:", key="j_plantas")
            st.radio("¿Necesita iluminación exterior tipo jardín?", ["Sí", "No"], key="j_luz")

        elif especialidad == "Climatización":
            st.subheader("2. Especificación de Climatización")
            st.selectbox("Tipo de sistema deseado:", ["Aire acondicionado split", "Aire acondicionado central", "Calefacción por radiadores", "Piso radiante", "Ventilación mecánica"], key="cl_sistema")
            st.number_input("Metros cuadrados (m²) a climatizar:", min_value=1.0, key="cl_m2")
            st.number_input("Número de ambientes o habitaciones:", min_value=1, key="cl_ambientes")
            st.text_input("Marca preferida (si la tiene):", key="cl_marca")
            st.radio("¿Requiere mantención de equipos existentes?", ["Sí", "No"], key="cl_mantencion")

        st.divider()
        
        # --- BOTÓN DE ENVIAR ---
        enviar = st.form_submit_button("🛠️ GENERAR ESPECIFICACIÓN TÉCNICA")
        
    if enviar:
        st.success("¡Cuestionario completado! Especificación generada.")
        st.balloons()
        st.write("**Próximo paso:** El sistema calculará los materiales basándose en estas respuestas y los conectará con tu archivo Excel.")
