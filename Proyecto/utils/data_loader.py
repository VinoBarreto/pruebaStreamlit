import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos(ruta):

    df = pd.read_csv(
        ruta,
        usecols=[
            "DR_NO",
            "DATE OCC",
            "TIME OCC",
            "AREA NAME",
            "Crm Cd Desc",
            "Vict Age",
            "Vict Sex",
            "Premis Desc",
            "Weapon Desc",
            "Status Desc",
            "LAT",
            "LON",
        ],
        parse_dates=["DATE OCC"],
        low_memory=False
    )

    df = df.dropna(subset=["LAT","LON"])
    df["Vict Age"] = pd.to_numeric(df["Vict Age"],errors="coerce")
    return df