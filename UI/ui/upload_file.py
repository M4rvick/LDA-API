import streamlit as st
import os
import tempfile

"""
    Este page se encarga de la carga de documentos, utiliza los paths locales
"""

def display_upload_section():

    st.header("Selecciona tus documentos")
    st.markdown("En formato `.txt` o `.pdf`. Puedes arrastrar y soltar múltiples archivos.")

    uploaded_files = st.file_uploader(
            "Haz click para agregar archivos o simplemente arrástralos",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        # Si se subieron archivos
    if uploaded_files:
        temp_dir = tempfile.mkdtemp()  # Carpeta temporal donde guardaremos los archivos subidos
        file_paths = []
        valid_files = []

        for file in uploaded_files:
            file_path = os.path.join(temp_dir, file.name)
            if file_path not in file_paths:
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                file_paths.append(file_path)
                valid_files.append(file)
                st.write(f"- `{file.name}` ({file.size} bytes)")
            else: st.warning(f"El archivo `{file.name}` ya fue existe.")
            

        # Guardamos las rutas absolutas en el estado de sesión
        st.session_state.uploaded_files = valid_files
        st.session_state.document_paths = file_paths

        st.success(f"¡Se cargaron {len(valid_files)} documento(s) exitosamente! Puede proceder a configurar los parametros en la pestaña 'Configurar Modelo'")

    else:
        # Limpiar estado si no hay archivos
        st.session_state.uploaded_files = None
        st.session_state.document_paths = []
        st.session_state.processing_complete = False
        st.session_state.mock_results = None  
