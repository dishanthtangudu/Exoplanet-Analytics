import os
import pandas as pd
import streamlit as st

from csv_manager import CSVManager


def apply_style():
    st.markdown("""
    <style>

    /* Hide only Deploy button */
    [data-testid="stAppDeployButton"] {
        display: important;
    }

    /* Keep the three-dot menu */
    [data-testid="stToolbar"] {
        display: flex !important;
        visibility: visible !important;
    }

    /* Main background */
    .stApp {
        background-color: #F7F3EA;
        color: #172033;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E8E1D5;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #172033 !important;
    }

    /* Input text */
    input,
    textarea {
        color: #172033 !important;
        background-color: white !important;
    }

    /* Select boxes */
    [data-baseweb="select"] {
        background-color: white !important;
    }

    [data-baseweb="select"] * {
        color: #172033 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: white;
        color: #172033;
        border: 1px solid #B8B0A3;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #F0ECE4;
        color: #172033;
        border-color: #172033;
    }

    /* Form buttons */
    [data-testid="stFormSubmitButton"] button {
        background-color: white;
        color: #172033;
        border: 1px solid #B8B0A3;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        background-color: white;
    }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background-color: white;
        color: #172033;
        border: 1px solid #B8B0A3;
    }

    </style>
    """, unsafe_allow_html=True)


def show(fig):
    fig.update_layout(
        template="simple_white",
        paper_bgcolor="#F7F3EA",
        plot_bgcolor="white",
        font=dict(color="#172033"),
        title_font=dict(color="#172033"),
        xaxis=dict(
            title_font=dict(color="#172033"),
            tickfont=dict(color="#172033")
        ),
        yaxis=dict(
            title_font=dict(color="#172033"),
            tickfont=dict(color="#172033")
        ),
        legend=dict(
            font=dict(color="#172033")
        )
    )

    st.plotly_chart(fig, width="stretch")


def counts(series, name):
    result = (
        series
        .value_counts(dropna=False)
        .reset_index()
    )

    result.columns = [name, "Count"]

    return result


def input_field(label, config, key=None, value=None):
    field_type = config[0]

    if field_type == "text":
        return st.text_input(
            label,
            value="" if value is None else str(value),
            key=key
        )

    if field_type == "int":
        minimum = config[1]
        maximum = config[2]

        if value is None or pd.isna(value):
            current = minimum
        else:
            current = int(value)

        return st.number_input(
            label,
            min_value=minimum,
            max_value=maximum,
            value=current,
            step=1,
            key=key
        )

    if field_type == "float":
        minimum = config[1]
        maximum = config[2]

        if value is None or pd.isna(value):
            current = minimum
        else:
            current = float(value)

        return st.number_input(
            label,
            min_value=minimum,
            max_value=maximum,
            value=current,
            key=key
        )

    if field_type == "select":
        options = config[1]

        index = 0

        if value in options:
            index = options.index(value)

        return st.selectbox(
            label,
            options,
            index=index,
            key=key
        )


def crud_page(
    title,
    icon,
    filename,
    id_column,
    prefix,
    fields,
    analysis
):
    apply_style()

    st.title(f"{icon} {title}")

    file_path = os.path.join(
        "data",
        filename
    )

    # Required CSV columns
    columns = [
        id_column
    ] + [
        column
        for column in fields.keys()
        if column != id_column
    ]

    manager = CSVManager(
        file_path,
        columns
    )

    # ---------------- READ DATA ----------------

    try:
        df = manager.read_data()

    except FileNotFoundError:
        st.error(
            f"CSV file not found: {filename}"
        )
        return

    except pd.errors.EmptyDataError:
        st.error(
            "The CSV file is empty."
        )
        return

    except ValueError as e:
        st.error(str(e))
        return

    except Exception:
        st.error(
            "Unable to read the CSV file."
        )
        return

    # ---------------- SEARCH ----------------

    search = st.text_input(
        "🔎 Search",
        key=f"{prefix}_search"
    )

    filtered = df.copy()

    if search:
        mask = (
            filtered
            .astype(str)
            .apply(
                lambda column:
                column.str.contains(
                    search,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        )

        filtered = filtered[mask]

    # ---------------- FILTER ----------------

    filter_columns = [
        column
        for column in fields
        if column in filtered.columns
    ]

    if filter_columns:

        filter_column = st.selectbox(
            "🔽 Filter Column",
            ["None"] + filter_columns,
            key=f"{prefix}_filter_column"
        )

        if filter_column != "None":

            values = (
                filtered[filter_column]
                .dropna()
                .unique()
                .tolist()
            )

            if values:

                selected = st.selectbox(
                    "Filter Value",
                    ["All"] + values,
                    key=f"{prefix}_filter_value"
                )

                if selected != "All":

                    filtered = filtered[
                        filtered[filter_column] == selected
                    ]

    # ---------------- SORT ----------------

    if len(filtered.columns) > 0:

        sort_column = st.selectbox(
            "↕️ Sort By",
            filtered.columns,
            key=f"{prefix}_sort_column"
        )

        ascending = st.checkbox(
            "Ascending order",
            value=True,
            key=f"{prefix}_ascending"
        )

        filtered = filtered.sort_values(
            sort_column,
            ascending=ascending
        )

    # ---------------- DATA ----------------

    st.subheader("📋 Data")

    st.dataframe(
        filtered,
        hide_index=True,
        width="stretch"
    )

    # ---------------- CREATE ----------------

    st.subheader("➕ Create Record")

    with st.form(
        f"{prefix}_create_form"
    ):

        new_record = {}

        for column, config in fields.items():

            new_record[column] = input_field(
                column,
                config,
                key=f"{prefix}_create_field_{column}"
            )

        create_button = st.form_submit_button(
            "Create Record"
        )

        if create_button:

            try:

                record = {}

                for column in fields:
                    record[column] = new_record[column]

                manager.create_record(
                    record
                )

                st.success(
                    "Record created successfully."
                )

                st.rerun()

            except ValueError as e:

                st.error(str(e))

            except Exception:

                st.error(
                    "Unable to create the record."
                )

    # ---------------- UPDATE ----------------

    st.subheader("✏️ Update Record")

    if len(df) > 0:

        ids = (
            df[id_column]
            .astype(str)
            .tolist()
        )

        selected_id = st.selectbox(
            "Select Record",
            ids,
            key=f"{prefix}_selected_update_record"
        )

        old_row = df[
            df[id_column]
            .astype(str)
            == selected_id
        ].iloc[0]

        with st.form(
            f"{prefix}_update_form"
        ):

            updated_record = {}

            for column, config in fields.items():

                # Do not edit the ID
                if column == id_column:
                    continue

                updated_record[column] = input_field(
                    column,
                    config,
                    key=f"{prefix}_update_field_{column}",
                    value=old_row[column]
                )

            update_button = st.form_submit_button(
                "Update Record"
            )

            if update_button:

                try:

                    manager.update_record(
                        selected_id,
                        updated_record
                    )

                    st.success(
                        "Record updated successfully."
                    )

                    st.rerun()

                except ValueError as e:

                    st.error(str(e))

                except Exception:

                    st.error(
                        "Unable to update the record."
                    )

    # ---------------- DELETE ----------------

    st.subheader("🗑️ Delete Record")

    if len(df) > 0:

        delete_ids = (
            df[id_column]
            .astype(str)
            .tolist()
        )

        delete_id = st.selectbox(
            "Select Record to Delete",
            delete_ids,
            key=f"{prefix}_selected_delete_record"
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this record.",
            key=f"{prefix}_delete_confirmation"
        )

        if st.button(
            "Delete Record",
            key=f"{prefix}_delete_button"
        ):

            if not confirm:

                st.warning(
                    "Please confirm the deletion first."
                )

            else:

                try:

                    manager.delete_record(
                        delete_id
                    )

                    st.success(
                        "Record deleted successfully."
                    )

                    st.rerun()

                except ValueError as e:

                    st.error(str(e))

                except Exception:

                    st.error(
                        "Unable to delete the record."
                    )

    # ---------------- ANALYSIS ----------------

    st.subheader("📊 Analysis")

    if len(filtered) > 0:

        analysis(filtered)

    else:

        st.info(
            "No records available for analysis."
        )

    # ---------------- EXPORT ----------------

    st.subheader("⬇️ Export")

    csv_data = filtered.to_csv(
        index=False
    )

    st.download_button(
        "Download CSV",
        csv_data,
        file_name=f"{prefix}_filtered.csv",
        mime="text/csv",
        key=f"{prefix}_download_csv"
    )