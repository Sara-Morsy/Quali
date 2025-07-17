import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Dashboard.csv")  # replace with your file
df = load_data()

# App title
st.title("Simple User Interface to Explore current qualitative research used in clinical trials")

# --- Search Bar Only ---
search_id = st.text_input("Search by ID (partial or full match):").strip().lower()

# --- Filtered Data Based on Search ---
filtered_df = df.copy()
if search_id:
    filtered_df = filtered_df[filtered_df["ID"].str.lower().str.contains(search_id)]

# --- Display Results ---
st.subheader("Search Results")

if not filtered_df.empty:
    # Add clickable hyperlinks for ID
    def make_clickable(id_val):
        return f'<a href="?selected_id={id_val}">{id_val}</a>'

    table_display = filtered_df.copy()
    table_display["ID"] = table_display["ID"].apply(make_clickable)

    # Show as HTML table with clickable links
    st.markdown(table_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No data found for the search term.")

# --- Selected ID Detail View ---
selected_id = st.query_params.get("selected_id")
if selected_id:
    st.markdown(f"### Full Entry for ID: `{selected_id}`")
    full_data = df[df["ID"] == selected_id]
    if not full_data.empty:
        st.dataframe(full_data.reset_index(drop=True))
    else:
        st.warning("No data found for this ID.")
