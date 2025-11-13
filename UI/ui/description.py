import streamlit as st

def set_page_upload():
    st.session_state.page = "main"

def display_description_section():
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: left; font-size: 70px;'>Modelado de temas en texto utilizando LDA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size: 32px; color: gray;'>LatentVies es un utiliza LDA (Latent Dirichlet Allocation) para determinar los temas ocultos en un corpus de texto.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size: 32px; color: gray;'>¡Empieza ahora cargando tus documentos!</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button(
            "Cargar documentos", 
            width='stretch', 
            type="tertiary",
            on_click=set_page_upload  
        )