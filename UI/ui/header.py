import streamlit as st

def set_page_main():
    st.session_state.page = "main"

def set_page_home():
    st.session_state.page = "intro"

def set_page_description():
    st.session_state.page = "description"

def display_header():
    """
    Streamlit no soporta headers "fijos" (sticky) por defecto, pero
    al ser lo primero que se dibuja, siempre estará en la parte superior.
    """
    # Usamos columnas para alinear el logo a la izquierda y los enlaces a la derecha
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.button("LatentView", 
                  icon=":material/view_in_ar:", 
                  type="primary", 
                  width="content",
                  on_click=set_page_home
                  )

    with col2:
        links_cols = st.columns(5)
        with links_cols[2]:
            st.button("¿Qué es LatentView?", 
                      type="secondary", 
                      width="content",
                      on_click=set_page_description)
        with links_cols[3]:
            st.button("Carga de Documentos", 
                      type="secondary", 
                      width="content",
                      on_click=set_page_main)
        with links_cols[4]:
            st.button("Soporte", 
                      type="tertiary", 
                      width="content")
    # vista de divisiion
    st.markdown(" ")
