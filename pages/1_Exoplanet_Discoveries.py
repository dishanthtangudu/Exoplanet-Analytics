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
    # Summary metrics
    a, b, c = st.columns(3)

    a.metric("Exoplanets", len(df))
    b.metric(
        "Confirmed",
        (df["koi_disposition"] == "CONFIRMED").sum()
    )
    c.metric("Average Score", round(df["koi_score"].mean(), 2))

    # Disposition and score distribution
    l, r = st.columns(2)

    with l:
        show(px.pie(
            counts(df["koi_disposition"], "Disposition"),
            names="Disposition",
            values="Count",
            title="Exoplanet Disposition"
        ))

    with r:
        show(px.histogram(
            df,
            x="koi_score",
            nbins=10,
            title="Kepler Score Distribution"
        ))

    # Scatter plot and discoveries by year
    l, r = st.columns(2)

    with l:
        planet_df = df.dropna(
            subset=["koi_period", "koi_prad"]
        )

        show(px.scatter(
            planet_df,
            x="koi_period",
            y="koi_prad",
            color="koi_disposition",
            title="Orbital Period vs Planet Radius",
            labels={
                "koi_period": "Orbital Period (days)",
                "koi_prad": "Planet Radius (Earth radii)",
                "koi_disposition": "Disposition"
            }
        ))

    with r:
        year_df = df.dropna(subset=["koi_year"]).copy()

        if not year_df.empty:
            year_counts = (
                year_df.groupby("koi_year")
                .size()
                .reset_index(name="Count")
                .sort_values("koi_year")
            )

            year_counts["koi_year"] = (
                year_counts["koi_year"].astype(int)
            )

            show(px.line(
                year_counts,
                x="koi_year",
                y="Count",
                markers=True,
                title="Exoplanet Discoveries by Year",
                labels={
                    "koi_year": "Discovery Year",
                    "Count": "Number of Exoplanets"
                }
            ))
        else:
            st.info("No discovery-year data is available.")


crud_page(
    "Exoplanet Discoveries",
    "🪐",
    "exoplanet_discoveries.csv",
    "kepoi_name",
    "E",
    FIELDS,
    analysis
)
