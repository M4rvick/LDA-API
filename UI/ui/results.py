import streamlit as st
import pandas as pd
import numpy as np
import pyLDAvis
import plotly.express as px
import streamlit.components.v1 as components

def display_results_section(results):

    """
    Muestra los resultados reales del modelo LDA devueltos por la API.
    Se basa en la estructura del JSON que retorna la API
    """

    st.header("Resultados del Modelado de Tópicos")

    if not results or "results" not in results:
        st.info("No hay resultados disponibles. Ejecuta el procesamiento desde la pestaña 'Configurar Modelo'.")
        return

    lda_data = results["results"]

    #1. Visualizaacion de configuracion del modelo
    if "config" in lda_data:
        st.subheader("Configuración del Modelo")
        config = lda_data["config"]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Número de tópicos", config.get("n_topics", "-"))
        with col2:
            st.metric("Alpha", config.get("alpha", "-"))
        with col3:
            st.metric("Beta", config.get("eta", "-"))
        with col4:
            st.metric("Tamaño del vocabulario", config.get("vocab_size", "-"))
        with col5:
            st.metric("Número de documentos", config.get("n_documents", "-"))

        st.markdown("---")

    #2. Palabras clave por tópico 
    if "topics" in lda_data:
        st.subheader("Palabras clave por Tópico Identificado")
        st.markdown("Haz clic en cada tópico para ver todas sus palabras clave.")

        topics = lda_data["topics"]

        for topic_id, topic_data in topics.items():
            top_words = topic_data.get("top_words", [])
            with st.expander(f"Tópico {topic_id}", 
                            expanded=True):
                st.markdown(", ".join(top_words))

    # 3. Distribución de tópicos por documento
    if "document_topics" in lda_data:
        st.subheader("Distribución de Tópicos por Documento")

        doc_topics = lda_data["document_topics"]

        # Convertir a DataFrame
        rows = []
        for doc_name, doc_info in doc_topics.items():
            row = {"Documento": doc_name}
            topic_dist = doc_info.get("topic_distribution", [])
            for i, prob in enumerate(topic_dist):
                row[f"Tópico {i}"] = prob
            row["Tópico dominante"] = doc_info.get("dominant_topic", "-")
            row["Probabilidad dominante"] = doc_info.get("dominant_topic_prob", "-")
            rows.append(row)

        df_doc_topics = pd.DataFrame(rows)
        df_doc_topics = df_doc_topics.set_index("Documento")

        st.markdown("Probabilidad estimada de que cada tópico aparezca en cada documento.")

        # Detectar columnas de probabilidad 
        prob_cols = [col for col in df_doc_topics.columns if "Tópico" in col and "dominante" not in col]
        prob_cols.append("Probabilidad dominante")

        # Aplicar formato solo a las columnas de probabilidad 
        st.dataframe(
            df_doc_topics.style.format(
                {col: "{:.2%}" for col in prob_cols}  
            )
        )


        # # Mostrar el topico dominante
        # topics = lda_data["topics"]
        # dominant = str(doc_info.get("dominant_topic"))
        # top_words = topics[dominant].get("top_words", [])
        # with st.expander(f"Tópico {dominant} dominante", 
        #                    expanded=True):
        #     st.markdown(", ".join(top_words))

        # --- 4. Gráfico de prevalencia global ---
        # topic_prevalence = df_doc_topics[[col for col in df_doc_topics.columns if "Tópico" in col and "dominante" not in col]].mean()
        # st.bar_chart(topic_prevalence)

        #4. Gráfico de prevalencia global 
        st.subheader("Prevalencia Global de Tópicos")
        st.markdown("Porcentaje promedio de aparición de cada tópico en el conjunto de documentos.")

        topic_prevalence = df_doc_topics[
            [col for col in df_doc_topics.columns if "Tópico" in col and "dominante" not in col]
        ].mean().reset_index()

        topic_prevalence.columns = ["Tópico", "Prevalencia"]
        topic_prevalence = topic_prevalence.sort_values("Prevalencia", ascending=False)

        # Grafica con plotly
        fig = px.bar(
            topic_prevalence,
            x="Prevalencia",
            y="Tópico",
            orientation="h",
            text=topic_prevalence["Prevalencia"].apply(lambda x: f"{x:.2%}"),
            color="Prevalencia",
            color_continuous_scale="Blues",
            title="Distribución de Prevalencia de Tópicos",
        )

        # Ajustes visuales
        fig.update_layout(
            xaxis_title="Porcentaje promedio",
            yaxis_title="Tópico",
            title_x=0.5,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14),
        )
        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, width='stretch')
         # Extraer información relevante
        topics = lda_data["topics"]
        doc_topics = lda_data["document_topics"]

        # Matriz de distribución documento-tópico
        topic_distributions = [doc_info["topic_distribution"] for doc_info in doc_topics.values()]
        topic_matrix = np.array(topic_distributions)

        # Vocabulario por tópico (top words)
        topic_words = [", ".join(topics[t]["top_words"]) for t in topics.keys()]

        # Crear una estructura mínima de datos para visualización
        topic_prevalence = topic_matrix.mean(axis=0)
        df_topics = pd.DataFrame({
            "Tópico": [f"Tópico {i}" for i in range(len(topic_prevalence))],
            "Prevalencia": topic_prevalence,
            "Palabras clave": topic_words
        })

        # Mostrar en tabla
        st.dataframe(df_topics)

    else:
        st.info("No se encontraron distribuciones de tópicos por documento.")
