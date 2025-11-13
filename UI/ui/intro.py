import streamlit as st

#definicion para el boton de iniciar.
def set_page_main():
    st.session_state.page = "main"

def display_intro_section():
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>LDA: LatentView</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 32px; color: gray;'>Descubre los temas que las palabras ocultan en tu texto</p>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button(
            "Iniciar", 
            width='stretch', 
            type="tertiary",
            on_click=set_page_main  
        )