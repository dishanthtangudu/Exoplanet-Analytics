import plotly.express as px
import streamlit as st

from utils import crud_page, counts, show

FIELDS = {
    "name": ("text",),
    "id": ("int", 1, 100000),
    "nametype": ("select", ["Valid", "Relict"]),
    "recclass": ("text",),
    "mass": ("float", 0.0, 10000000.0),
    "fall": ("select", ["Fell", "Found"]),
    "year": ("int", 1500, 2100),
    "reclat": ("float", -90.0, 90.0),
    "reclong": ("float", -180.0, 180.0),
}


def analysis(df):
    a, b, c = st.columns(3)

    a.metric("Meteorites", len(df))
    b.metric("Classes", df["recclass"].nunique())
    c.metric("Fell", (df["fall"] == "Fell").sum())

    l, r = st.columns(2)

    with l:
        show(
            px.pie(
                counts(df["fall"], "Fall"),
                names="Fall",
                values="Count",
                title="Meteorite Fall Status"
            )
        )

    with r:
        top_classes = (
            df["recclass"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_classes.columns = ["Class", "Count"]

        show(
            px.bar(
                top_classes,
                x="Class",
                y="Count",
                title="Top Meteorite Classes"
            )
        )

    show(
        px.histogram(
            df,
            x="year",
            nbins=20,
            title="Meteorite Discoveries by Year",
            labels={"year": "Year"}
        )
    )

    mass_df = df.dropna(subset=["mass"])

    show(
        px.histogram(
            mass_df,
            x="mass",
            nbins=20,
            title="Meteorite Mass Distribution",
            labels={"mass": "Mass (g)"}
        )
    )


crud_page(
    "Discovery Methods",
    "🔭",
    "meteorite_landings.csv",
    "id",
    "M",
    FIELDS,
    analysis
)