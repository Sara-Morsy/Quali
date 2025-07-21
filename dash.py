import streamlit as st
import pandas as pd

# Load data from GitHub raw URL
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Sara-Morsy/Quali/main/Dashboard.csv"
    return pd.read_csv(url)

df = load_data()

# App title
st.title("Explore Qualitative Research in Clinical Trials")

# --- Search Bar ---
search_id = st.text_input("Search by ID (partial or full match):").strip().lower()

# --- Filtered Results ---
filtered_df = df.copy()
if "ID" in df.columns and search_id:
    filtered_df = filtered_df[filtered_df["ID"].astype(str).str.lower().str.contains(search_id)]

# --- Display Results ---
st.subheader("Search Results")

if not filtered_df.empty:
    def make_clickable(id_val):
        return f'<a href="?selected_id={id_val}">{id_val}</a>'

    table_display = filtered_df.copy()
    if "ID" in table_display.columns:
        table_display["ID"] = table_display["ID"].apply(make_clickable)

    st.markdown(table_display.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No data found for the search term.")

# --- Selected ID Detail View ---
selected_id = st.query_params.get("selected_id")
if selected_id:
    st.markdown(f"### Full Entry for ID: `{selected_id}`")
    full_data = df[df["ID"].astype(str) == selected_id]
    if not full_data.empty:
        st.dataframe(full_data.reset_index(drop=True))
    else:
        st.warning("No data found for this ID.")
