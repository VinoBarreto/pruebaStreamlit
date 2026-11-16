import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import folium

from streamlit_folium import st_folium

st.set_page_config(
    page_title="Sistema de Análisis de Incidentes", layout="wide")

st.title("Sistema de Análisis de Incidentes Geolocalizados")
st.caption("Dashboard análitico con visualización estadística,temporal e histórica")

# Configuración de Tema para Seaborn
plt.style.use("dark_background")

sns.set_theme(
    style="darkgrid",
    palette="rocket",
    rc={
        "axes.facecolor": "#0e1117",
        "figure.facecolor": "#0e1117",
        "grid.color": "#2a2a2a",
        "axes.edgecolor": "#444444",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
    }
)

ruta = "data/incidents.csv"

df = cargar_datos(ruta)

f1, f2, f3 = st.columns(3)

anios = sorted(df["DATE OCC"].dt.year.dropna().unique())
area_policial = sorted(df["AREA NAME"].dropna().unique())

with f1:
    seleccion_anios = st.multiselect(
        "Años",
        anios,
        default=[max(anios)]
    )
with f2:
    seleccion_area_p = st.multiselect(
        "Área Policial",
        area_policial,
        default=area_policial[:3]
    )
with f3:
    st.metric("Total registros: ", len(df))


if (not seleccion_anios) or (not seleccion_area_p):
    st.warning("Debe elegir al menos un año y un area policial")
    st.stop()

df_filtrado = df[
    (df["DATE OCC"].dt.year.isin(seleccion_anios)) &
    (df["AREA NAME"].isin(seleccion_area_p))
]


k1, k2, k3 = st.columns(3)

k1.metric("Indicentes: ", len(df_filtrado))
k2.metric("Delito más frecuente: ", df_filtrado["Crm Cd Desc"].mode()[0])
k3.metric("Área crítica: ", df_filtrado["AREA NAME"].mode()[0])


g1, g2 = st.columns(2)

with g1:
    st.subheader("Incidentes por tipo")
    top_crimenes = df_filtrado["Crm Cd Desc"].value_counts().head(
        10).reset_index()
    top_crimenes.columns = ["Tipo", "Cantidad"]
    fig = px.bar(
        top_crimenes,
        x="Cantidad",
        y="Tipo",
        orientation="h",
        hover_data=["Tipo", "Cantidad"]
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


with g2:
    st.subheader("Distribución de edad de las víctimas...")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.violinplot(
        data=df_filtrado,
        x="Vict Sex",
        y="Vict Age",
        inner="quartile",
        linewidth=1.2,
        ax=ax
    )

    sns.stripplot(
        data=df_filtrado,
        x="Vict Sex",
        y="Vict Age",
        color="white",
        alpha=0.25,
        size=2,
        ax=ax
    )

    ax.set_xlabel("Sexo")
    ax.set_ylabel("Edad")

    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig)

g3, g4 = st.columns(2)

with g3:
    st.subheader("Evolucion Temporal")
    tiempo_df = (
        df_filtrado
        .groupby(df_filtrado["DATE OCC"].dt.to_period("M"))
        .size()
        .reset_index(name="Incidentes")
    )
    tiempo_df["DATE OCC"] = tiempo_df["DATE OCC"].dt.to_timestamp()

    fig = px.line(
        tiempo_df,
        x="DATE OCC",
        y="Incidentes"
    )
    st.plotly_chart(fig)


with g4:
    st.subheader("Incidentes por área")

    area_df = (
        df_filtrado["AREA NAME"]
        .value_counts()
        .reset_index()
    )
    area_df.columns = ["Área", "Incidentes"]

    chart = alt.Chart(area_df).mark_bar().encode(
        x=alt.X("Área:N", sort="-y"),
        y="Incidentes:Q",
        tooltip=["Área", "Incidentes"]
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

mapa_df = df_filtrado.sample(
    min(2500, len(df_filtrado))
)

areas_unicas = mapa_df["AREA NAME"].unique()

paleta = [
    "#4cc9f0", "#f72585", "#b5179e", "#7209b7",
    "#560bad", "#480ca8", "#3a0ca3", "#3f37c9",
    "#4361ee", "#4895ef", "#4ea8de", "#56cfe1"
]

mapa_colores = {
    area: paleta[i % len(paleta)] for i, area in enumerate(areas_unicas)
}

st.write(mapa_colores)


mapa = folium.Map(
    location=[mapa_df["LAT"].mean(), mapa_df["LON"].mean()],
    zoom_start=10,
    tile="CartoDB positron"
)

grupo_marcadores = folium.FeatureGroup(name="Incidentes")
for _, row in mapa_df.iterrows():
    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=5,
        color=mapa_colores[row["AREA NAME"]],
        fill=True,
        fill_color=mapa_colores[row["AREA NAME"]],
        fill_opacity=0.7,
        popup=f"""
        <b>Área policial:</b> {row['AREA NAME']}<br>
        <b>Tipo:</b> {row['Crm Cd Desc']}<br>
        <b>Fecha:</b> {row['DATE OCC'].date()}<br>
        <b>Sexo víctima:</b> {row['Vict Sex']}<br>
        <b>Edad víctima:</b> {row['Vict Age']}
        """
    ).add_to(grupo_marcadores)

grupo_marcadores.add_to(mapa)

legend_html = """
<div style="
position: fixed;
bottom: 40px;
left: 40px;
width: 260px;
background-color: rgba(14,17,23,0.9);
border-radius: 8px;
padding: 10px;
font-size: 13px;
color: white;
z-index: 9999;
">
<b>Áreas policiales</b><br>
"""
for area, color in mapa_colores.items():
    legend_html += f"""
    <i style="
        background:{color};
        width:10px;
        height:10px;
        display:inline-block;
        margin-right:6px;
        border-radius:50%;
    "></i>{area}<br>
    """
legend_html += "</div>"

mapa.get_root().html.add_child(folium.Element(legend_html))

st_folium(
    mapa,
    use_container_width=True,
    returned_objects=[]
)
