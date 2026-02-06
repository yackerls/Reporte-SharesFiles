import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Reporte-SharesFiles", layout="wide")

st.title("📂 Auditoría de Carpetas Compartidas")
st.markdown("---")

# Lista negra de identidades de sistema
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
    # Cargar datos
    df = pd.read_csv(uploaded_file)
    
    # Limpieza inicial: Quitar espacios y filtrar usuarios de sistema
    df['Identity'] = df['Identity'].str.strip()
    df_clean = df[~df['Identity'].isin(SISTEMA_EXCLUDE)].copy()

    # --- SECCIÓN DE FILTROS (Igual a la versión anterior) ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        # Filtro multiselect por nombre de carpeta (ShareName)
        share_filter = st.multiselect("Filtrar por Share:", options=sorted(df_clean['ShareName'].unique().tolist()))
    with col_f2:
        # Buscador por texto (Usuario o Carpeta)
        search_query = st.text_input("Buscar Usuario o Carpeta específica:")

    # Aplicar la lógica de los filtros sobre los datos ya limpios
    if share_filter:
        df_clean = df_clean[df_clean['ShareName'].isin(share_filter)]
    
    if search_query:
        # Busca en todas las columnas para no limitar la experiencia
        mask = df_clean.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        df_clean = df_clean[mask]

    # --- VISUALIZACIÓN ---
    st.subheader("Resultados de Auditoría")
    
    # Métricas rápidas
    c1, c2, c3 = st.columns(3)
    c1.metric("Shares encontrados", df_clean['ShareName'].nunique())
    c2.metric("Usuarios/Grupos", df_clean['Identity'].nunique())
    c3.metric("Total registros", len(df_clean))

    # Tabla de resultados
    st.dataframe(df_clean, use_container_width=True, hide_index=True)
    
    # Gráfica profesional (Top 10 usuarios con más carpetas asignadas)
    st.markdown("### Análisis de Accesos")
    top_acc = df_clean['Identity'].value_counts().head(10).reset_index()
    top_acc.columns = ['Usuario/Grupo', 'Conteo']
    fig = px.bar(top_acc, x='Conteo', y='Usuario/Grupo', orientation='h', 
                 title="Top 10 Usuarios con más asignaciones",
                 color='Conteo', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Por favor, sube el archivo para comenzar. Los usuarios de sistema (SYSTEM, Administrators, etc.) se filtran automáticamente.")