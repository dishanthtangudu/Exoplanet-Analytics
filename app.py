import streamlit as st

from utils import apply_style

st.set_page_config(
    page_title="Exoplanet Analytics",
    page_icon="🪐",
    layout="wide"
)

apply_style()

st.title("🪐 Exoplanet Analytics")

st.write(
    "A simple data analytics dashboard for exploring "
    "exoplanets and astronomical data."
)

st.subheader("📚 Project Modules")

st.info(
    "Use the sidebar to open and explore the different "
    "project modules."
)

st.write("### Available Modules")

c1, c2 = st.columns(2)

with c1:
    st.info("🪐 **Exoplanet Discoveries**")
    st.write(
        "exoplanet candidates, dispositions, "
        "scores, orbital periods, and planet radius."
    )

    st.info("📊 **Exoplanet Characteristics**")
    st.write(
       "Features and Characterstics of Exoplanets"
    )

with c2:
    st.info("☄️ **Meteorite Landings**")
    st.write(
        "Analyze meteorite classes, masses, fall status, "
        "locations, and landing years."
    )

    st.info("📍**Astronomical Facilities**")
    st.write(
        "Explore Astronomical Facilities types, magnitudes, locations, "
        "and durations."
    )

st.divider()

st.subheader("🔬 About the Project")

st.write(
    "This project uses CSV datasets to demonstrate "
    "CRUD operations, data analysis, and interactive "
    "visualization using Python, Pandas, NumPy, Plotly, "
    "and Streamlit."
)
