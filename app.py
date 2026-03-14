import streamlit as st
from koboextractor import KoboExtractor
import pandas as pd

TOKEN    = "23801d339dd6d16509a79250731f126401d5f7a3"
BASE_URL = "https://kobo.humanitarianresponse.info/api/v2"
asset_uid = "afWux6DQFqmZrEpK54BobD"

def load_kobo_data():
    kobo = KoboExtractor(TOKEN, BASE_URL)
    start, limit, all_records = 0, 1000, []
    while True:
        data    = kobo.get_data(asset_uid, start=start, limit=limit)
        records = data["results"]
        if not records:
            break
        all_records.extend(records)
        start += limit

    df = pd.json_normalize(all_records)

    # Rename BEFORE stripping group prefix
    df = df.rename(columns={
        'group_og9hq60/asha':       'asha',
        'group_og9hq60/Paticipant': 'Paticipant'
    })
    df.columns = [
        col if col in ['asha', 'Paticipant']
        else col.split('/')[-1]
        for col in df.columns
    ]
    return df

# ── Init / Refresh ──────────────────────────────────────
if "df" not in st.session_state:
    with st.spinner("Loading data..."):
        st.session_state.df = load_kobo_data()

if st.button("🔄 Refresh Kobo Data"):
    with st.spinner("Fetching latest data..."):
        st.session_state.df = load_kobo_data()
    st.success("Refreshed!")

df = st.session_state.df
st.title("आशा मॉनिटरिंग डॅशबोर्ड")

# ── Guard ───────────────────────────────────────────────
for col in ['asha', 'Paticipant', '_submission_time']:
    if col not in df.columns:
        st.error(f"Column '{col}' not found. Check KoboToolbox field names.")
        st.stop()

st.write("एकूण नोंदी:", df.shape[0])

# ── Dates ───────────────────────────────────────────────
df['_submission_time'] = pd.to_datetime(df['_submission_time'])
df['Month']     = df['_submission_time'].dt.strftime('%b')
df['Month_num'] = df['_submission_time'].dt.month

# ── Table 1 : ASHA × Month ──────────────────────────────
st.subheader("तक्ता १: आशा फॉर्म भरलेले कॅलेंडर टेबल")
table1 = pd.pivot_table(
    df, index='asha', columns='Month',
    values='Paticipant', aggfunc='count', fill_value=0
)
month_order = (df[['Month','Month_num']].drop_duplicates()
               .sort_values('Month_num')['Month'])
table1 = table1.reindex(columns=month_order)
table1['एकूण'] = table1.sum(axis=1)   # ← Total column
st.dataframe(table1, use_container_width=True)

# ── Duplicates ──────────────────────────────────────────
dup = df[df.duplicated(subset=['asha','Paticipant'], keep=False)]

# ── Table 2 : Duplicate Count ───────────────────────────
st.subheader("तक्ता २: आशानुसार एकाच सहभागीची अनेक नोंदी संख्या")
table2 = (dup.groupby('asha')['Paticipant']
            .count()
            .reset_index(name='Duplicate Entries')
            .sort_values('Duplicate Entries', ascending=False))
st.dataframe(table2, use_container_width=True)

# ── Table 3 : Duplicate Detail ──────────────────────────
st.subheader("तक्ता ३: आशानुसार एकाच सहभागीच्या अनेक नोंदींची यादी")
if len(dup) > 0:
    selected_asha = st.selectbox("ASHA निवडा", sorted(dup['asha'].unique()))
    table3 = (dup[dup['asha'] == selected_asha]
              [['asha','Paticipant','_submission_time']]
              .sort_values('Paticipant')
              .copy())
    table3['नोंदी संख्या'] = (table3.groupby('Paticipant')['Paticipant']
                               .transform('count'))
    st.dataframe(table3, use_container_width=True)
else:
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.")
