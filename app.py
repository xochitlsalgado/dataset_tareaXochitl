import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Airbnb Dashboard", layout="wide")

st.title("🚀 Airbnb Data Dashboard")

# Carga de datos
try:
    df = pd.read_csv("airbnb_data.csv") # El nombre debe ser igual al de tu archivo
    
    # Sidebar para filtros
    st.sidebar.header("Filtros")
    room_types = st.sidebar.multiselect("Tipo de habitación:", 
                                        options=df["room_type"].unique(),
                                        default=df["room_type"].unique())
    
    df_selection = df[df["room_type"].isin(room_types)]

    # Gráficas
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(df_selection, x="neighbourhood", y="price", title="Precio por Barrio")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.scatter(df_selection, x="longitude", y="latitude", color="price", title="Mapa de Calor de Precios")
        st.plotly_chart(fig2, use_container_width=True)

    st.write("### Tabla de Datos", df_selection.head())

except Exception as e:
    st.error(f"Error: No se encontró el archivo csv o las columnas no coinciden. {e}")