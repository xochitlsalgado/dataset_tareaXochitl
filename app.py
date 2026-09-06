import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Airbnb Data Analytics", layout="wide")

st.title("Airbnb Dataset")
st.markdown("Análisis visual de alojamientos y precios")
st.markdown("---")

# Carga de datos
@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")  
    return df

try:
    df = load_data()

    # --- BARRA LATERAL (Filtros) ---
    st.sidebar.header("Panel de Filtros")
    
    # Filtro de Precio
    min_price = int(df["price"].min())
    max_price = int(df["price"].max())
    price_range = st.sidebar.slider("Rango de Precio ($)", min_price, max_price, (min_price, 1000))

    # Filtro de Barrios
    barrios_disponibles = df["neighbourhood"].unique()
    barrios = st.sidebar.multiselect("Selecciona Barrios:", 
                                     options=barrios_disponibles, 
                                     default=barrios_disponibles[:5])

    # Aplicar filtros
    df_selection = df[(df["price"] >= price_range[0]) & 
                      (df["price"] <= price_range[1]) & 
                      (df["neighbourhood"].isin(barrios))]

    # --- MÉTRICAS TOP ---
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Alojamientos", len(df_selection))
    col_b.metric("Precio Promedio", f"${df_selection['price'].mean():.2f}")
    
    if not df_selection.empty:
        col_c.metric("Barrio más caro", df_selection.groupby("neighbourhood")["price"].mean().idxmax())
    else:
        col_c.metric("Barrio más caro", "N/A")
        
    col_d.metric("Reseñas Totales", f"{int(df_selection['number_of_reviews'].sum())}")

    st.markdown("---")

    # --- GRÁFICAS PRINCIPALES ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Distribución de Precios")
        # Gráfica de caja para ver la dispersión de precios
        fig_box = px.box(df_selection, x="room_type", y="price", color="room_type",
                         title="Análisis de Precios por Tipo de Habitación",
                         template="plotly_dark")
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.subheader("🏠 Tipos de Habitación")
        # NUEVA GRÁFICA: Gráfica de pastel en lugar del mapa
        fig_pie = px.pie(df_selection, names="room_type", 
                         title="Proporción de Oferta por Tipo",
                         hole=0.4, # Hace que sea tipo "Donut" que se ve más moderno
                         template="plotly_dark",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- GRÁFICA INFERIOR ---
    st.subheader("📈 Popularidad: Precio vs Número de Reseñas")
    # Gráfica de dispersión para ver si lo más caro es lo más reseñado
    fig_scatter = px.scatter(df_selection, x="price", y="number_of_reviews", 
                             color="room_type", size="availability_365",
                             hover_name="neighbourhood",
                             title="Relación entre Precio y Cantidad de Reseñas",
                             template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabla de datos al final
    with st.expander(" Ver tabla de datos filtrados"):
        st.write(df_selection)

except Exception as e:
    st.error(f"Error al cargar la aplicación: {e}")