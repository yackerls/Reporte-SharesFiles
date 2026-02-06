import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Reporte Shares", layout="wide")
st.title("📂 Auditoría de Carpetas Compartidas")

PATH_DATA = "data/permisos_shares.csv"

if os.path.exists(PATH_DATA):
    df = pd.read_csv(PATH_DATA)
    
    # Dashboard de métricas
    c1, c2 = st.columns(2)
    c1.metric("Total de Shares", df['ShareName'].nunique())
    c2.metric("Usuarios únicos con acceso", df['Identity'].nunique())

    # Gráfica Profesional
    st.subheader("Distribución de Permisos por Grupo/Usuario")
    fig = px.pie(df, names='AccessType', title="Tipos de Acceso (Allow/Deny)", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # Buscador Profesional
    st.subheader("🔍 Buscador de Permisos")
    search = st.text_input("Ingrese nombre de usuario o carpeta:")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)
else:
    st.error("Archivo 'data/permisos_shares.csv' no encontrado. Sube el reporte para comenzar.")