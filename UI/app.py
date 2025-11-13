import streamlit as st
import time
import pandas as pd
import numpy as np

from ui import header, intro, description, upload_file, params, results

st.set_page_config(
    page_title="LDA: LatentView",
    page_icon="images/icon.png", 
    layout="wide"
)

#estilos de buttons
st.markdown("""
<style>
    div.stButton > button {
        border: none !important;
        outline: none !important;
        background-color: transparent !important; /* fondo transparente */
        color: #222 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }

    /* Hover para botones normales (no terciarios) */
    div.stButton > button:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
        color: #0078ff !important;
    }

    div.stButton > button[kind="tertiary"] {
        background-color: black !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 6px 18px !important;
        transition: background-color 0.3s ease !important;
    }

    div.stButton > button[kind="tertiary"]:hover {
        background-color: #333 !important;
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)


#inicialiacion de las variables de estado, sirven para mantenerse en un lugar y no crear un bucle
if 'page' not in st.session_state:
    st.session_state.page = "intro" #inicia mostrando la bienvenida
if 'description' not in st.session_state:
    st.session_state.description = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'lda_params' not in st.session_state:
    st.session_state.lda_params = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'api_results' not in st.session_state: #se cambia el mock por el api
    st.session_state.api_results = None

#se carag el header
header.display_header()
# Renderizar el contenido de la barra lateral
# with st.sidebar:
#     st.title("LatentView")
#     st.markdown("---")
#     st.header("¿Qué es LatentView?")
#     st.info("""
#     LatentView es una herramienta que utiliza LDA (Latent Dirichlet Allocation) 
#     para determinar los temas ocultos en un corpus de texto.
#     """)
#     st.header("Soporte")
#     st.markdown("Para ayuda o preguntas, contacte a [soporte@latentview.com](mailto:soporte@latentview.com).")
#navegacion

if st.session_state.page == "intro":
    intro.display_intro_section()
if st.session_state.page == "description":
    description.display_description_section()
elif st.session_state.page == "main":
    tab_upload, tab_params, tab_results = st.tabs([
        "1. Cargar Documentos", 
        "2. Configurar Modelo", 
        "3. Visualizar Resultados"
    ])

    #carga de files
    with tab_upload:
        upload_file.display_upload_section()
    
    #hiperparametros
    with tab_params:
        if st.session_state.uploaded_files:
            params.display_parameters_section()
        else:
            st.warning("Por favor, cargar el corpus previamente.")

    #ver resulktadpos
    with tab_results:
        if st.session_state.processing_complete:
            if st.session_state.api_results:
                st.success("¡Procesamiento completado!")
                results.display_results_section(st.session_state.api_results)
            else:
                st.warning("No se encontraron resultados en memoria. Verifica la ejecución del modelo.")
        else:
            st.info("Por favor, configura los parámetros y ejecuta el modelo para ver los resultados.")