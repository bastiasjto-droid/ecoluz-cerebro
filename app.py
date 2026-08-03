import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cerebro ECOLUZ")

st.title("🧠 Cerebro de Especificaciones Técnicas")

# Menú principal
opcion = st.selectbox("¿Qué especialidad vamos a revisar?", 
                      ["Selecciona...", "Electricidad", "Construcción", "Paisajismo", "Generadores"])

if opcion != "Selecciona...":
    st.subheader(f"Cuestionario para {opcion}")
    
    with st.form("cuestionario"):
        if opcion == "Electricidad":
            voltaje = st.selectbox("¿Voltaje del proyecto?", ["110V", "220V", "380V"])
            circuitos = st.number_input("¿Cuantos circuitos independientes?", min_value=1, step=1)
            tierra = st.radio("¿Necesita puesta a tierra?", ["Sí", "No"])
        
        elif opcion == "Construcción":
            superficie = st.number_input("Superficie total a construir (m²)", min_value=1.0, step=1.0)
            terreno = st.selectbox("Tipo de terreno", ["Plano", "Irregular", "Pendiente"])
            muros = st.selectbox("Material de muros", ["Ladrillo", "Bloque", "Concreto"])
            
        enviar = st.form_submit_button("Generar Especificación")
        
    if enviar:
        st.success("¡Especificación generada! (Aquí iría tu lógica de cálculo)")
        st.write("Próximo paso: conectar con el Excel para sacar los materiales.")
