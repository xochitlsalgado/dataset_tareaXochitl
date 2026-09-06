import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Ancho completo)
st.set_page_config(page_title="Airbnb Premium Dashboard", layout="wide")

# Estilo personalizado con Markdown para que se vea más pro
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Airbnb Data Analysis Pro")
st.markdown("---")

# Carga de datos
@st.cache_data
def load_data():
    df = pd.read_csv("AB_NYC_2019.csv")
    return df

try:
    df = load_data()

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2560px-Airbnb_Logo_B%C3%A9lo.svg.png", width=150)
    st.sidebar.header("Panel de Filtros")
    
    # Filtro de Precio con Slider
    min_price = int(df["price"].min())
    max_price = int(df["price"].max())
    price_range = st.sidebar.slider("Rango de Precio ($)", min_price, max_price, (min_price, 500))

    # Filtro de Barrios
    barrios = st.sidebar.multiselect("Selecciona Barrios:", options=df["neighbourhood"].unique(), default=df["neighbourhood"].unique()[:3])

    # Aplicar filtros
    df_selection = df[(df["price"] >= price_range[0]) & 
                      (df["price"] <= price_range[1]) & 
                      (df["neighbourhood"].isin(barrios))]

    # --- MÉTRICAS TOP ---
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Listings", len(df_selection))
    col_b.metric("Precio Promedio", f"${df_selection['price'].mean():.2f}")
    col_c.metric("Barrio más caro", df_selection.groupby("neighbourhood")["price"].mean().idxmax())
    col_d.metric("Disponibilidad Prom.", f"{int(df_selection['availability_365'].mean())} días")

    st.markdown("---")

    # --- GRÁFICAS ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💰 Distribución de Precios por Tipo")
        fig_box = px.box(df_selection, x="room_type", y="price", color="room_type",
                         points="all", title="Precios vs Tipo de Habitación")
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.subheader("📍 Mapa de Localización")
        # Mapa con color basado en el precio
        fig_map = px.scatter_mapbox(df_selection, lat="latitude", lon="longitude", color="price", 
                                     size="price", color_continuous_scale=px.colors.cyclical.IceFire, 
                                     size_max=15, zoom=10, mapbox_style="carto-positron",
                                     hover_name="neighbourhood")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    # --- SECCIÓN EXTRA ---
    st.subheader("📈 Top 10 Barrios por cantidad de ofertas")
    top_barrios = df_selection["neighbourhood"].value_counts().head(10).reset_index()
    top_barrios.columns = ["Barrio", "Cantidad"]
    fig_bar = px.bar(top_barrios, x="Barrio", y="Cantidad", color="Cantidad", color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Mostrar tabla con estilo
    with st.expander("👀 Ver datos crudos filtrados"):
        st.dataframe(df_selection)

except Exception as e:
    st.error(f"Error al cargar la visualización: {e}")