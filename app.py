import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría NTFS - Limpieza de Sistema", layout="wide")

st.title("📂 Auditoría de Carpetas Compartidas")
st.markdown("---")

# Lista de exclusión definitiva para limpiar el reporte
SISTEMA_EXCLUDE = [
    'NT AUTHORITY\\SYSTEM',
    'BUILTIN\\Administrators',
    'CREATOR OWNER',
    'BUILTIN\\Users',
    'Everyone',
    'NT AUTHORITY\\Authenticated Users'
]

uploaded_file = st.file_uploader("Subir archivo permisos_shares.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Limpieza de datos (quitar espacios y filtrar)
    df['Identity'] = df['Identity'].str.strip()
    df_clean = df[~df['Identity'].isin(SISTEMA_EXCLUDE)].copy()

    # Dashboard de métricas con datos reales
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Shares", df_clean['ShareName'].nunique())
    c2.metric("Usuarios/Grupos Reales", df_clean['Identity'].nunique())
    c3.metric("Entradas Filtradas", len(df_clean))

    # Gráfica Profesional de Accesos Reales
    st.subheader("Concentración de Accesos (Usuarios Reales)")
    top_acc = df_clean['Identity'].value_counts().head(12).reset_index()
    top_acc.columns = ['Usuario/Grupo', 'Cantidad']
    
    fig = px.bar(top_acc, x='Cantidad', y='Usuario/Grupo', orientation='h',
                 color='Cantidad', color_continuous_scale='Reds',
                 title="Identidades con más acceso a Shares")
    st.plotly_chart(fig, use_container_width=True)

    # Explorador de Datos
    st.subheader("🔍 Buscador de Permisos")
    search = st.text_input("Buscar por nombre de usuario o carpeta:")
    
    if search:
        # Filtrado dinámico en todas las columnas
        df_clean = df_clean[df_clean.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    st.dataframe(df_clean, use_container_width=True, hide_index=True)
    
else:
    st.info("Suba el CSV. Se están omitiendo automáticamente: SYSTEM, Administrators y otros grupos de sistema.")