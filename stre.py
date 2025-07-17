import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Final_dt.csv")  # replace with your file
df = load_data()

# App title
st.title("Simple User Interface to Explore DigiTwin")

# --- Search Bar ---
search_id = st.text_input("Search by ID (partial or full match):").strip().lower()

# --- Filter Options ---
col1, col2 = st.columns(2)
with col1:
    domain_options = sorted(df[df["node"] == "Scientific domain"]["value"].dropna().unique())
    selected_domain = st.selectbox("Scientific Domain", [""] + domain_options)

with col2:
    node_options = sorted(df["node"].dropna().unique())
    selected_node = st.selectbox("Node", [""] + node_options)

# --- Apply Filters ---
filtered_df = df.copy()

if search_id:
    filtered_df = filtered_df[filtered_df["ID"].str.lower().str.contains(search_id)]

if selected_domain:
    domain_ids = df[(df["node"] == "Scientific domain") & (df["value"] == selected_domain)]["ID"].unique()
    filtered_df = filtered_df[filtered_df["ID"].isin(domain_ids)]

if selected_node:
    filtered_df = filtered_df[filtered_df["node"] == selected_node]

# --- View Switch ---
view_mode = st.radio("View Mode", ["Results Table", "Graph"])

# --- Results Table View ---
if view_mode == "Results Table":
    st.subheader("Filtered Results")

    if not filtered_df.empty:
        # Add clickable hyperlinks for ID
        def make_clickable(id_val):
            return f'<a href="?selected_id={id_val}">{id_val}</a>'

        table_display = filtered_df.copy()
        table_display["ID"] = table_display["ID"].apply(make_clickable)

        # Show as HTML table with clickable links
        st.markdown(table_display.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("No data found for the current filters.")

    # --- Selected ID View ---
    selected_id = st.query_params.get("selected_id")
    if selected_id:
        st.markdown(f"### Full Entry for ID: `{selected_id}`")
        full_data = df[df["ID"] == selected_id]
        if not full_data.empty:
            st.dataframe(full_data.reset_index(drop=True))
        else:
            st.warning("No data found for this ID.")

# --- Graph View ---
elif view_mode == "Graph":
    st.subheader("Summary of Values")

    if selected_node and not filtered_df.empty:
        value_counts = filtered_df["value"].value_counts().reset_index()
        value_counts.columns = ["Value", "Count"]

        fig, ax = plt.subplots()
        ax.pie(value_counts["Count"], labels=value_counts["Value"], autopct='%1.1f%%', startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    elif not selected_node:
        st.info("Please select a node to view a graph.")
    else:
        st.info("No data available for the selected filters.")

