import streamlit as st
import time
import requests
import json

"""
    El usuario condigura los parametros del modelo o los deja por defecto, aqui se envia la peticion y se reciben los resultados en formato JSON
"""

API_URL = "http://127.0.0.1:8000/process-documents" #url del servidor local 

def display_parameters_section():
    
    st.header("Ajuste de Hiperparámetros del Modelo LDA")
    st.markdown("""
    Configura los parámetros para el algoritmo Latent Dirichlet Allocation (LDA). 
    El número de tópicos (K) es el parámetro más importante a definir.
    """)

    # formulario
    with st.form(key="lda_params_form"):
        
        st.subheader("Modificación de parámetros básicos")
        
        # Slider para el número de temas (K)
        num_topics = st.slider(
            "Número de Tópicos (K)", 
            min_value=2, 
            max_value=15, 
            value=5, 
            help="Define cuántos temas distintos quieres que el modelo identifique."
        )
        
        st.subheader("Parámetros Avanzados (Opcional)")
        st.markdown("""
            Puede modificar el numnero de Tópicos y el número de Repeticiones.
        """)
        st.markdown("""
            Los hiperparámetros α y β estan optimizados para obtener el mejor resultado y ser autoajustables, puede configurarlos si es necesario.
        """)
        st.markdown("""
                    
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Alpha: Densidad de temas por documento
            alpha = st.number_input(
                "Alpha (Document-Topic Density)", 
                min_value=0.01, 
                max_value=50.0, 
                value=50.0, 
                step=0.01,
                format="%.2f",
                help="Valores bajos significan que los documentos tienen pocos temas. Alpha se autojusta por defecto siguiendo la regla de α= (50/#Topicos), a menos que se inserte un parametro especifico."
            )
        
        with col2:
            beta = st.number_input(
                "Beta (Topic-Word Density)", 
                min_value=0.01, 
                max_value=30.0, 
                value=0.01, 
                step=0.01,
                format="%.2f",
                help="Valores bajos significan que los temas tienen pocas palabras clave."
            )
            
        passes = st.number_input(
            "Número de Repeticiones (Epochs)", 
            min_value=1, 
            max_value=150, 
            value=100,
            help="Cuántas veces el modelo verá el corpus completo durante el entrenamiento."
        )

        process_button = st.form_submit_button(
            label="Generar Tópicos",
            type="primary",
            width='stretch'
        )

    if process_button:
        lda_params = {
            "document_paths": st.session_state.document_paths,
            "num_topics": num_topics,
            'alpha': alpha,
            "eta": beta,
            "n_iterations":passes,
        }

        try:
            with st.spinner("Procesando documentos..."):
                response = requests.post(API_URL, json=lda_params)

            if response.status_code == 200:
                st.success("Procesamiento completado exitosamente.")
                st.session_state.processing_complete = True
                st.session_state.api_results = response.json()

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f" No se pudo conectar con el servidor.\n\nDetalles: {e}")


