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

st.write("Dataset shape:", df.shape)

# =====================
# Convert submission time
# =====================

df['_submission_time'] = pd.to_datetime(df['_submission_time'])

df['Month'] = df['_submission_time'].dt.strftime('%b')
df['Month_num'] = df['_submission_time'].dt.month

# =====================
# TABLE 1 : ASHA × MONTH
# =====================

table1 = pd.pivot_table(
    df,
    index='asha',
    columns='Month',
    values='Paticipant',
    aggfunc='count',
    fill_value=0
)

month_order = (
    df[['Month','Month_num']]
    .drop_duplicates()
    .sort_values('Month_num')['Month']
)

table1 = table1.reindex(columns=month_order)

st.subheader("Table 1: ASHA Month-wise Form Count")
st.dataframe(table1)

# =====================
# FIND DUPLICATES
# =====================

dup = df[df.duplicated(
    subset=['asha','Paticipant'],
    keep=False
)]

# =====================
# TABLE 2
# =====================

table2 = (
    dup.groupby('asha')['Paticipant']
    .nunique()
    .reset_index(name='Duplicate Participants')
)

st.subheader("Table 2: Duplicate Participants by ASHA")
st.dataframe(table2)

# =====================
# TABLE 3
# =====================

asha_list = dup['asha'].unique()

selected_asha = st.selectbox("Select ASHA", asha_list)

table3 = dup[dup['asha'] == selected_asha][
    ['asha','Paticipant','_submission_time']
]

st.subheader("Table 3: Duplicate List")
st.dataframe(table3)


