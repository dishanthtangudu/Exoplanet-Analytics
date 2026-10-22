import pandas as pd
import plotly.express as px
import streamlit as st

from utils import crud_page, counts, show


# Columns available in ExoPlanet_characterstics.csv
FIELDS = {
    "pl_name": ("text",),
    "hostname": ("text",),
    "pl_rade": ("float", 0.0, 1000.0),
    "pl_bmasse": ("float", 0.0, 1000000.0),
    "pl_orbper": ("float", 0.0, 10000000.0),
    "pl_eqt": ("float", 0.0, 100000.0),
    "discoverymethod": ("text",),
    "disc_year": ("int", 1800, 2100),
    "disc_facility": ("text",),
}


def analysis(df):
    """Show summary metrics and charts for the selected exoplanet records."""

    st.subheader("Planetary Characteristics")

    total_planets = len(df)
    average_radius = df["pl_rade"].mean()
    average_mass = df["pl_bmasse"].mean()
    methods = df["discoverymethod"].nunique()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Exoplanets", f"{total_planets:,}")
    c2.metric(
        "Average Radius",
        "N/A" if pd.isna(average_radius) else f"{average_radius:.2f} Earth radii",
    )
    c3.metric(
        "Average Mass",
        "N/A" if pd.isna(average_mass) else f"{average_mass:.2f} Earth masses",
    )
    c4.metric("Discovery Methods", methods)

    st.caption(
        "Radius is measured in Earth radii, mass in Earth masses, "
        "orbital period in days, and equilibrium temperature in Kelvin. "
        "Some planets do not have every measurement recorded."
    )

    st.subheader("Planet Size and Mass")

    left, right = st.columns(2)

    with left:
        radius_df = df.dropna(subset=["pl_rade"])
        if not radius_df.empty:
            show(
                px.histogram(
                    radius_df,
                    x="pl_rade",
                    nbins=30,
                    title="Exoplanet Radius Distribution",
                    labels={"pl_rade": "Radius (Earth radii)"},
                )
            )
        else:
            st.info("No radius measurements are available for these records.")

    with right:
        mass_df = df.dropna(subset=["pl_bmasse"])
        if not mass_df.empty:
            show(
                px.histogram(
                    mass_df,
                    x="pl_bmasse",
                    nbins=30,
                    title="Exoplanet Mass Distribution",
                    labels={"pl_bmasse": "Mass (Earth masses)"},
                )
            )
        else:
            st.info("No mass measurements are available for these records.")

    size_mass_df = df.dropna(subset=["pl_rade", "pl_bmasse"])
    if not size_mass_df.empty:
        show(
            px.scatter(
                size_mass_df,
                x="pl_rade",
                y="pl_bmasse",
                color="discoverymethod",
                hover_name="pl_name",
                title="Planet Radius vs Mass",
                labels={
                    "pl_rade": "Radius (Earth radii)",
                    "pl_bmasse": "Mass (Earth masses)",
                    "discoverymethod": "Discovery Method",
                },
            )
        )

    st.subheader("Orbit and Temperature")

    left, right = st.columns(2)

    with left:
        orbit_df = df.dropna(subset=["pl_orbper"])
        if not orbit_df.empty:
            show(
                px.histogram(
                    orbit_df,
                    x="pl_orbper",
                    nbins=30,
                    title="Orbital Period Distribution",
                    labels={"pl_orbper": "Orbital Period (days)"},
                )
            )
        else:
            st.info("No orbital-period measurements are available.")

    with right:
        temp_df = df.dropna(subset=["pl_eqt"])
        if not temp_df.empty:
            show(
                px.histogram(
                    temp_df,
                    x="pl_eqt",
                    nbins=30,
                    title="Equilibrium Temperature Distribution",
                    labels={"pl_eqt": "Temperature (K)"},
                )
            )
        else:
            st.info("No temperature measurements are available.")

    st.subheader("Discovery Information")

    left, right = st.columns(2)

    with left:
        method_counts = counts(df["discoverymethod"], "Discovery Method")
        show(
            px.bar(
                method_counts,
                x="Discovery Method",
                y="Count",
                title="Exoplanets by Discovery Method",
            )
        )

    with right:
        year_counts = (
            df["disc_year"]
            .dropna()
            .astype(int)
            .value_counts()
            .sort_index()
            .reset_index()
        )
        year_counts.columns = ["Discovery Year", "Count"]
        show(
            px.line(
                year_counts,
                x="Discovery Year",
                y="Count",
                markers=True,
                title="Exoplanet Discoveries by Year",
            )
        )


crud_page(
    "Exoplanet Characteristics",
    "🪐",
    "ExoPlanet_characterstics.csv",
    "pl_name",
    "EC",
    FIELDS,
    analysis,
)
