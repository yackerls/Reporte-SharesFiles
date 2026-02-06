import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría NTFS - Carga Manual", layout="wide")

st.title("📂 Auditoría de Carpetas Compartidas")
st.markdown("---")

# Componente para subir el archivo manualmente
uploaded_file = st.file_uploader("Subir archivo permisos_shares.csv generado en Windows", type=["csv"])

if uploaded_file is not None:
    # Leer el archivo subido
    df = pd.read_csv(uploaded_file)
    
    # KPIs Rápidos
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Shares", df['ShareName'].nunique())
    c2.metric("Usuarios/Grupos Únicos", df['Identity'].nunique())
    c3.metric("Registros de Permisos", len(df))

    # Gráfica Profesional
    st.subheader("Concentración de Accesos por Identidad")
    top_acc = df['Identity'].value_counts().head(10).reset_index()
    top_acc.columns = ['Usuario/Grupo', 'Cantidad']
    fig = px.bar(top_acc, x='Cantidad', y='Usuario/Grupo', orientation='h', 
                 color='Cantidad', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    # Buscador y Filtros
    st.subheader("🔍 Explorador de Permisos")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        share_filter = st.multiselect("Filtrar por Share:", options=sorted(df['ShareName'].unique().tolist()))
    with col_f2:
        search_user = st.text_input("Buscar Usuario (Identity):")

    # Aplicar filtros
    if share_filter:
        df = df[df['ShareName'].isin(share_filter)]
    if search_user:
        df = df[df['Identity'].str.contains(search_user, case=False, na=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Opción para descargar lo que se está viendo
    st.download_button("Descargar Vista Actual (CSV)", df.to_csv(index=False), "reporte_filtrado.csv")

else:
    st.info("Por favor, sube el archivo CSV para visualizar los datos de Share and Storage Management.")