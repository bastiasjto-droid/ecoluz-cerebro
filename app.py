import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cerebro ECOLUZ", layout="wide")
st.title("🧠 Cerebro de Especificaciones Técnicas")

# Menú principal
especialidad = st.selectbox("Selecciona la especialidad:", 
                            ["Selecciona...", "Construcción Nueva", "Remodelación", "Reparación", "Mantención"])

if especialidad != "Selecciona...":
    
    st.header(f"📋 Cuestionario para: {especialidad}")
    
    with st.form("cuestionario_completo"):
        st.subheader("1. Información General")
        tipo_trabajo = st.selectbox("¿Qué tipo de trabajo necesita?", ["Construcción nueva", "Remodelación", "Ampliación", "Reparación", "Mantención"])
        ubicacion = st.text_input("¿Dónde está ubicada la obra?")
        tamanio = st.number_input("¿Cuál es el tamaño aproximado del proyecto? (m²)", min_value=1.0, step=1.0)
        planos = st.radio("¿Tiene planos o diseño?", ["Sí", "No"])
        permisos = st.radio("¿Cuenta con permisos municipales?", ["Sí", "No", "En trámite"])
        presupuesto = st.number_input("¿Cuál es el presupuesto aproximado? (CLP)", min_value=0, step=100000)
        inicio = st.text_input("¿Cuándo desea comenzar? (Ej: Agosto 2026)")
        plazo = st.text_input("¿Cuál es el plazo esperado para terminar? (Ej: 3 meses)")

        st.divider()

        # Solo mostramos las preguntas de construcción si el usuario elige Construcción Nueva (para no hacerla eterna en una sola prueba)
        if especialidad == "Construcción Nueva":
            st.subheader("2. Terreno")
            terreno_limpio = st.radio("¿El terreno está limpio?", ["Sí", "No"])
            terreno_tipo = st.selectbox("¿El terreno es plano o tiene pendiente?", ["Plano", "Pendiente suave", "Pendiente pronunciada"])
            acceso_maquinaria = st.radio("¿Hay acceso para maquinaria?", ["Sí", "No"])
            servicios = st.radio("¿Cuenta con agua y electricidad en el terreno?", ["Sí", "No"])

            st.subheader("3. Cimientos")
            fundacion = st.selectbox("¿Qué tipo de fundación desea?", ["Corrida", "Aislada", "Losa de fundación", "No sé"])
            estudio_suelo = st.radio("¿Se realizará estudio de suelo?", ["Sí", "No"])
            
            st.subheader("4. Materiales de construcción")
            tipo_construccion = st.selectbox("¿Qué tipo de construcción desea?", ["Albañilería", "Hormigón", "Metalcon", "Madera", "Panel SIP"])
            
            if tipo_construccion == "Albañilería":
                ladrillo = st.selectbox("¿Utilizará ladrillo fiscal o princesa?", ["Ladrillo Fiscal", "Ladrillo Princesa"])
                estuco_interior = st.radio("¿Llevará estuco interior?", ["Sí", "No"])
                estuco_exterior = st.radio("¿Llevará estuco exterior?", ["Sí", "No"])
                estuco_tipo = st.selectbox("El estuco será:", ["Fino", "Grueso"])
                impermeabilizante = st.radio("¿Se aplicará impermeabilizante?", ["Sí", "No"])
                
            elif tipo_construccion == "Hormigón":
                hormigon_tipo = st.selectbox("¿Hormigón armado o prefabricado?", ["Hormigón Armado", "Prefabricado"])
                resistencia = st.text_input("¿Qué resistencia del hormigón utilizará? (Ej: H20, H30)")
                
            elif tipo_construccion == "Metalcon":
                espesor_perfiles = st.text_input("¿Qué espesor de perfiles? (Ej: 90mm, 150mm)")
                aislacion_termica = st.radio("¿Llevará aislación térmica?", ["Sí", "No"])
                revestimiento_metalcon = st.text_input("¿Qué tipo de revestimiento utilizará? (Ej: Placa exterior, OSB)")

            st.subheader("5. Techumbre")
            techo_tipo = st.selectbox("¿Qué tipo de techo desea?", ["Cubierta de Zinc", "Teja", "PV4", "Teja Asfáltica"])
            aislacion_techo = st.radio("¿Llevará aislación en el techo?", ["Sí", "No"])
            canaletas = st.radio("¿Instalará canaletas?", ["Sí", "No"])
            cielo_falso = st.radio("¿Llevará cielo falso?", ["Sí", "No"])

            st.subheader("6. Muros")
            muros_espesor = st.text_input("¿Qué espesor tendrán los muros? (Ej: 15cm)")
            cadenas = st.radio("¿Llevarán cadenas y pilares?", ["Sí", "No"])
            revestimiento_interior = st.text_input("¿Qué revestimiento interior desea? (Ej: Yeso cartón)")
            revestimiento_exterior = st.text_input("¿Qué revestimiento exterior desea? (Ej: Revestimiento PVC)")

            st.subheader("7. Terminaciones")
            piso_tipo = st.selectbox("¿Qué tipo de piso instalará?", ["Cerámica", "Porcelanato", "Piso flotante", "Vinílico", "Radier afinado"])
            pintura_tipo = st.text_input("¿Qué tipo de pintura utilizará? (Interior/Exterior)")
            yeso = st.radio("¿Llevará yeso?", ["Sí", "No"])
            guardapolvos = st.radio("¿Instalará guardapolvos?", ["Sí", "No"])
            puertas_tipo = st.text_input("¿Qué tipo de puertas?")
            ventanas_tipo = st.selectbox("¿Qué tipo de ventanas?", ["Aluminio", "PVC"])
            vidrio_tipo = st.selectbox("¿Vidrio simple o termopanel?", ["Vidrio Simple", "Termopanel"])

            st.subheader("8. Instalaciones")
            st.markdown("**Eléctrica:**")
            enchufes = st.number_input("¿Cuántos enchufes necesita?", min_value=0, step=1)
            interruptores = st.number_input("¿Cuántos interruptores?", min_value=0, step=1)
            luminarias = st.number_input("¿Cuántas luminarias?", min_value=0, step=1)
            tablero_nuevo = st.radio("¿Habrá tablero nuevo?", ["Sí", "No"])
            aumento_potencia = st.radio("¿Se solicitará aumento de potencia?", ["Sí", "No"])

            st.markdown("**Agua y Alcantarillado:**")
            agua_tipo = st.radio("¿Instalación de agua fría o caliente?", ["Solo agua fría", "Agua fría y caliente"])
            calefon = st.text_input("¿Qué tipo de calefón o termo usará?")
            alcantarillado = st.radio("¿Conexión existente o hay que instalar nuevas cámaras?", ["Conexión existente", "Instalar nuevas cámaras"])
            fosas = st.radio("¿Habrá fosa séptica?", ["Sí", "No"])

            st.subheader("9. Logística y Entrega")
            materiales_propiedad = st.radio("¿Quién proporcionará los materiales?", ["Cliente", "Contratista"])
            calidad_materiales = st.selectbox("¿Desea materiales económicos, estándar o premium?", ["Económicos", "Estándar", "Premium"])
            mano_obra = st.radio("¿Solo necesita mano de obra o con materiales incluidos?", ["Solo mano de obra", "Mano de obra + Materiales"])
            retiro_escombros = st.radio("¿Habrá retiro de escombros?", ["Sí", "No"])
            limpieza_final = st.radio("¿Desea limpieza final?", ["Sí", "No"])
            
            st.subheader("10. Detalles Técnicos Adicionales")
            radier_espesor = st.text_input("¿Qué espesor tendrá el radier? (Ej: 10cm)")
            malla_acma = st.radio("¿Llevará malla ACMA?", ["Sí", "No"])
            normativa = st.text_input("¿Qué norma de construcción se seguirá?")
            certificacion_SEC = st.radio("¿Se necesita certificación SEC para instalación eléctrica?", ["Sí", "No"])

        # Botón de enviar
        enviar = st.form_submit_button("🛠️ GENERAR ESPECIFICACIÓN TÉCNICA COMPLETA")
        
    if enviar:
        st.success("¡Especificación generada exitosamente!")
        st.balloons()
        st.write("Próximo paso: Conectar con el archivo Excel para calcular materiales, cantidades y precios.")
