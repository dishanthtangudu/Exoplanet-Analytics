
import pandas as pd
import plotly.express as px
import streamlit as st

from utils import crud_page, counts, show


FIELDS = {
    "name": ("text",),
    "source_url": ("text",),
    "osm_id": ("text",),
    "geometry_type": ("select", ["Point"]),
    "longitude": ("float", -180.0, 180.0),
    "latitude": ("float", -90.0, 90.0),
    "operator": ("text",),
    "access": ("select", [
        "private", "yes", "customers", "permit",
        "no", "permissive", "unknown"
    ]),
    "website": ("text",),
    "wheelchair": ("text",),
    "opening_hours": ("text",),
    "ref": ("text",),
    "fee": ("text",),
    "surface": ("text",),
}


def analysis(df):
    total = len(df)

    websites = (
        df["website"].fillna("").astype(str).str.strip() != ""
    ).sum()

    operators = (
        df["operator"].fillna("").astype(str).str.strip() != ""
    ).sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Facilities", total)
    col2.metric("Facilities with Websites", int(websites))
    col3.metric("Known Operators", int(operators))

    st.subheader("Facility Locations")

    map_df = df.dropna(subset=["latitude", "longitude"]).copy()
    map_df["latitude"] = pd.to_numeric(
        map_df["latitude"], errors="coerce"
    )
    map_df["longitude"] = pd.to_numeric(
        map_df["longitude"], errors="coerce"
    )
    map_df = map_df.dropna(subset=["latitude", "longitude"])

    if not map_df.empty:
        fig = px.scatter_geo(
            map_df,
            lat="latitude",
            lon="longitude",
            hover_name="name",
            hover_data=["operator", "access"],
            title="Astronomical Observatory Locations",
        )
        show(fig)
    else:
        st.info("No valid coordinates are available.")

    left, right = st.columns(2)

    with left:
        access = (
            df["access"]
            .fillna("Not specified")
            .replace("", "Not specified")
        )
        show(px.bar(
            counts(access, "Access"),
            x="Access",
            y="Count",
            title="Facilities by Access",
        ))

    with right:
        operator_data = (
            df["operator"].fillna("").astype(str).str.strip()
        )
        operator_data = operator_data[operator_data != ""]

        if not operator_data.empty:
            top_operators = (
                operator_data.value_counts()
                .head(10)
                .reset_index()
            )
            top_operators.columns = ["Operator", "Count"]

            show(px.bar(
                top_operators,
                x="Operator",
                y="Count",
                title="Top 10 Operators",
            ))
        else:
            st.info("No operator information is available.")

    st.subheader("Facilities by Latitude")

    latitude_df = df.dropna(subset=["latitude"])
    if not latitude_df.empty:
        show(px.histogram(
            latitude_df,
            x="latitude",
            nbins=20,
            title="Latitude Distribution",
            labels={"latitude": "Latitude"},
        ))


crud_page(
    "Astronomical Facilities",
    "🔭",
    "astronomical_facilities.csv",
    "osm_id",
    "AF",
    FIELDS,
    analysis,
)
