import streamlit as st
import pandas as pd

st.title("ASHA Monitoring Dashboard")

# GitHub file link
github_url = "https://raw.githubusercontent.com/shrikantdeshmukh9766-ux/NEW_APP/ccfc25827b7b7e85bfcb74eca04c7a1def6e2002/Round-2Baseline_form_for_COPD_and_Asthma_survey_by_ASHA_2025-2027_-_all_versions_-_labels_-_2026-03-09-17-33-30.xlsx"
# Read file
if github_url.endswith(".csv"):
    df = pd.read_csv(github_url)
else:
    df = pd.read_excel(github_url)

# Convert submission time
df['_submission_time'] = pd.to_datetime(df['_submission_time'])

# Month column
df['Month'] = df['_submission_time'].dt.strftime('%b')

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# =========================
# TABLE 1
# =========================
st.subheader("Table 1: ASHA Month-wise Form Count")

table1 = pd.pivot_table(
    df,
    index='Select the Name of Asha',
    columns='Month',
    values='Select the Participant Unique Code',
    aggfunc='count',
    fill_value=0
)

table1 = table1.reindex(columns=month_order, fill_value=0)

st.dataframe(table1)

# =========================
# FIND DUPLICATES
# =========================
dup = df[df.duplicated(
    subset=['Select the Name of Asha','Select the Participant Unique Code'],
    keep=False
)]

# TABLE 2
st.subheader("Table 2: Duplicate Participants by ASHA")

table2 = (
    dup.groupby('Select the Name of Asha')
    ['Select the Participant Unique Code']
    .nunique()
    .reset_index(name='Duplicate Participants')
)

st.dataframe(table2)

# TABLE 3
st.subheader("Table 3: Actual Duplicate Participant List")

asha_list = dup['Select the Name of Asha'].unique()

selected_asha = st.selectbox("Select ASHA", asha_list)

table3 = dup[dup['Select the Name of Asha'] == selected_asha][
    ['Select the Name of Asha',
     'Select the Participant Unique Code',
     '_submission_time']
].sort_values(['Select the Participant Unique Code','_submission_time'])

st.dataframe(table3)

