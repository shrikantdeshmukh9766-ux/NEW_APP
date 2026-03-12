import streamlit as st
from koboextractor import KoboExtractor
import pandas as pd

TOKEN = "23801d339dd6d16509a79250731f126401d5f7a3"
BASE_URL = "https://kobo.humanitarianresponse.info/api/v2"
asset_uid = "afWux6DQFqmZrEpK54BobD"

# Function to download data
def load_kobo_data():

    kobo = KoboExtractor(TOKEN, BASE_URL)

    start = 0
    limit = 1000
    all_records = []

    while True:
        data = kobo.get_data(asset_uid, start=start, limit=limit)

        records = data["results"]

        if len(records) == 0:
            break

        all_records.extend(records)
        start += limit

    df = pd.json_normalize(all_records)

    return df


# =====================
# REFRESH BUTTON
# =====================

if "df" not in st.session_state:
    st.session_state.df = load_kobo_data()

if st.button("🔄 Refresh Kobo Data"):
    st.session_state.df = load_kobo_data()

df = st.session_state.df

st.write("Dataset shape:", df.columns)
