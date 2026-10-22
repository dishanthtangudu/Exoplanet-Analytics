import plotly.express as px
import streamlit as st
from utils import crud_page, counts, show

FIELDS = {
    "kepoi_name": ("text",),
    "koi_disposition": ("select", [
        "CONFIRMED", "CANDIDATE", "FALSE POSITIVE"
    ]),
    "koi_score": ("float", 0.0, 1.0),
    "koi_period": ("float", 0.0, 100000.0),
    "koi_prad": ("float", 0.0, 100.0),
    "koi_year": ("int", 1990, 2030)
}


def analysis(df):
    a, b, c = st.columns(3)
    a.metric("Exoplanets", len(df))
    b.metric("Confirmed", (df["koi_disposition"] == "CONFIRMED").sum())
    c.metric("Average Score", round(df["koi_score"].mean(), 2))

    l, r = st.columns(2)

    with l:
        show(px.pie(
            counts(df["koi_disposition"], "Disposition"),
            names="Disposition", values="Count",
            title="Exoplanet Disposition"
        ))

    with r:
        show(px.histogram(
            df, x="koi_score", nbins=10,
            title="Kepler Score Distribution"
        ))

    show(px.scatter(
        df.dropna(subset=["koi_period", "koi_prad"]),
        x="koi_period", y="koi_prad",
        color="koi_disposition",
        title="Orbital Period vs Planet Radius",
        labels={
            "koi_period": "Orbital Period (days)",
            "koi_prad": "Planet Radius",
            "koi_disposition": "Disposition"
        }
    ))


crud_page(
    "Exoplanet Discoveries",
    "🪐",
    "exoplanet_discoveries.csv",
    "kepoi_name",
    "E",
    FIELDS,
    analysis
)