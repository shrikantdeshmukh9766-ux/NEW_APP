import streamlit as st
from koboextractor import KoboExtractor
import pandas as pd

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="आशा मॉनिटरिंग डॅशबोर्ड",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# CUSTOM CSS
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #fda085 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

/* overlay for readability */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(0px);
    pointer-events: none;
    z-index: 0;
}

/* ── Header Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 70%, #533483 100%);
    border-radius: 24px;
    padding: 36px 40px;
    margin-bottom: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '🌸';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.15;
}

.hero-banner::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
    transform: rotate(15deg);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(90deg, #f093fb, #f5576c, #fda085, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
    line-height: 1.2;
}

.hero-subtitle {
    color: rgba(255,255,255,0.6);
    font-size: 14px;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.5px;
}

/* ── Metric Cards ── */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}

.metric-card {
    border-radius: 18px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
}

.metric-card-1 { background: linear-gradient(135deg, #667eea, #764ba2); }
.metric-card-2 { background: linear-gradient(135deg, #f093fb, #f5576c); }
.metric-card-3 { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.metric-card-4 { background: linear-gradient(135deg, #43e97b, #38f9d7); }

.metric-card::after {
    content: '';
    position: absolute;
    top: -30%;
    right: -10%;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
}

.metric-icon {
    font-size: 28px;
    margin-bottom: 10px;
    display: block;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: white;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 12px;
    color: rgba(255,255,255,0.8);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Section Cards ── */
.section-card {
    background: rgba(255,255,255,0.97);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.8);
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid #f0f0f0;
}

.section-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.icon-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.icon-pink   { background: linear-gradient(135deg, #f093fb, #f5576c); }
.icon-blue   { background: linear-gradient(135deg, #4facfe, #00f2fe); }

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}

.section-desc {
    font-size: 13px;
    color: #888;
    margin: 2px 0 0 0;
}

/* ── Refresh Button ── */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 28px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.5) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    border-radius: 12px !important;
    border: 2px solid #667eea !important;
    font-family: 'Baloo 2', sans-serif !important;
    background: white !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
}

/* ── Success / Info ── */
.stSuccess {
    border-radius: 12px !important;
    background: linear-gradient(135deg, #43e97b22, #38f9d722) !important;
    border-left: 4px solid #43e97b !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #667eea !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, #667eea, #f093fb, #fda085) !important;
    border-radius: 2px !important;
    margin: 24px 0 !important;
}

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.badge-warning {
    background: linear-gradient(135deg, #f093fb22, #f5576c22);
    color: #f5576c;
    border: 1px solid #f5576c44;
}

.badge-success {
    background: linear-gradient(135deg, #43e97b22, #38f9d722);
    color: #0b8a4e;
    border: 1px solid #43e97b44;
}

/* ── Hide Streamlit Defaults ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# =====================
# CONSTANTS
# =====================
TOKEN     = "23801d339dd6d16509a79250731f126401d5f7a3"
BASE_URL  = "https://kobo.humanitarianresponse.info/api/v2"
asset_uid = "afWux6DQFqmZrEpK54BobD"

# =====================
# LOAD DATA
# =====================
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

# =====================
# SESSION STATE
# =====================
if "df" not in st.session_state:
    with st.spinner("KoboToolbox मधून डेटा लोड होत आहे..."):
        st.session_state.df = load_kobo_data()

# =====================
# HERO HEADER
# =====================
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🌸 आशा मॉनिटरिंग डॅशबोर्ड</h1>
    <p class="hero-subtitle">KoboToolbox · रिअल-टाइम डेटा विश्लेषण · सहभागी नोंदी</p>
</div>
""", unsafe_allow_html=True)

# =====================
# REFRESH BUTTON
# =====================
col_btn, col_space = st.columns([1, 5])
with col_btn:
    if st.button("🔄 डेटा रिफ्रेश करा"):
        with st.spinner("नवीनतम डेटा आणत आहे..."):
            st.session_state.df = load_kobo_data()
        st.success("✅ डेटा यशस्वीरित्या अपडेट झाला!")

df = st.session_state.df

# =====================
# GUARD
# =====================
for col in ['asha', 'Paticipant', '_submission_time']:
    if col not in df.columns:
        st.error(f"⚠️ '{col}' कॉलम सापडला नाही. KoboToolbox फील्ड नावे तपासा.")
        st.stop()

# =====================
# DATE PROCESSING
# =====================
df['_submission_time'] = pd.to_datetime(df['_submission_time'])
df['Month']     = df['_submission_time'].dt.strftime('%b')
df['Month_num'] = df['_submission_time'].dt.month

# =====================
# DUPLICATE CALCULATION
# =====================
dup = df[df.duplicated(subset=['asha', 'Paticipant'], keep=False)]
total_asha        = df['asha'].nunique()
total_participants = df['Paticipant'].nunique()
total_duplicates  = len(dup)
dup_ashas         = dup['asha'].nunique()

# =====================
# METRIC CARDS
# =====================
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card metric-card-1">
        <span class="metric-icon">📋</span>
        <div class="metric-value">{df.shape[0]}</div>
        <div class="metric-label">एकूण नोंदी</div>
    </div>
    <div class="metric-card metric-card-2">
        <span class="metric-icon">👩‍⚕️</span>
        <div class="metric-value">{total_asha}</div>
        <div class="metric-label">एकूण आशा</div>
    </div>
    <div class="metric-card metric-card-3">
        <span class="metric-icon">👥</span>
        <div class="metric-value">{total_participants}</div>
        <div class="metric-label">अनन्य सहभागी</div>
    </div>
    <div class="metric-card metric-card-4">
        <span class="metric-icon">⚠️</span>
        <div class="metric-value">{total_duplicates}</div>
        <div class="metric-label">डुप्लिकेट नोंदी</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================
# TABLE 1 : ASHA × MONTH
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-purple">📅</div>
        <div>
            <p class="section-title">तक्ता १ · आशा फॉर्म भरलेले कॅलेंडर टेबल</p>
            <p class="section-desc">प्रत्येक महिन्यातील आशानिहाय सहभागी संख्या</p>
        </div>
    </div>
""", unsafe_allow_html=True)

table1 = pd.pivot_table(
    df, index='asha', columns='Month',
    values='Paticipant', aggfunc='count', fill_value=0
)
month_order = (
    df[['Month', 'Month_num']].drop_duplicates()
    .sort_values('Month_num')['Month']
)
table1 = table1.reindex(columns=month_order)
table1['🔢 एकूण'] = table1.sum(axis=1)
table1 = table1.sort_values('🔢 एकूण', ascending=False)

st.dataframe(
    table1.style
        .background_gradient(cmap='RdYlGn', subset=table1.columns[:-1])
        .background_gradient(cmap='Blues', subset=['🔢 एकूण'])
        .format("{:.0f}"),
    use_container_width=True,
    height=min(400, (len(table1) + 1) * 38 + 10)
)
st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 2 : DUPLICATE COUNT
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-pink">🔁</div>
        <div>
            <p class="section-title">तक्ता २ · आशानुसार डुप्लिकेट नोंदी संख्या</p>
            <p class="section-desc">एकाच सहभागीच्या अनेक नोंदी असलेल्या आशा</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if len(dup) > 0:
    table2 = (
        dup.groupby('asha').agg(
            डुप्लिकेट_नोंदी=('Paticipant', 'count'),
            अनन्य_सहभागी=('Paticipant', 'nunique')
        )
        .reset_index()
        .sort_values('डुप्लिकेट_नोंदी', ascending=False)
        .rename(columns={'asha': '👩‍⚕️ आशा नाव'})
    )

    st.dataframe(
        table2.style
            .background_gradient(cmap='OrRd', subset=['डुप्लिकेट_नोंदी'])
            .background_gradient(cmap='YlOrBr', subset=['अनन्य_सहभागी']),
        use_container_width=True,
        height=min(350, (len(table2) + 1) * 38 + 10)
    )
else:
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 3 : DUPLICATE DETAIL
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue">🔍</div>
        <div>
            <p class="section-title">तक्ता ३ · आशानुसार डुप्लिकेट यादी</p>
            <p class="section-desc">निवडलेल्या आशाच्या एकाच सहभागीच्या सर्व नोंदी</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if len(dup) > 0:
    col1, col2 = st.columns([2, 4])
    with col1:
        selected_asha = st.selectbox(
            "👩‍⚕️ आशा निवडा",
            sorted(dup['asha'].unique()),
            help="डुप्लिकेट नोंदी असलेल्या आशा"
        )

    table3 = (
        dup[dup['asha'] == selected_asha][['asha', 'Paticipant', '_submission_time']]
        .sort_values('Paticipant')
        .copy()
    )
    table3['नोंदी_संख्या'] = table3.groupby('Paticipant')['Paticipant'].transform('count')
    table3 = table3.rename(columns={
        'asha':             '👩‍⚕️ आशा',
        'Paticipant':       '👤 सहभागी',
        '_submission_time': '🕐 नोंद वेळ',
        'नोंदी_संख्या':       '🔢 एकूण नोंदी'
    })

    st.markdown(f"""
    <div style="margin: 12px 0 16px 0;">
        <span class="badge badge-warning">⚠️ {len(table3)} डुप्लिकेट नोंदी आढळल्या</span>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        table3.style
            .background_gradient(cmap='Reds', subset=['🔢 एकूण नोंदी'])
            .applymap(lambda _: 'background-color: #fff5f5', subset=['👤 सहभागी']),
        use_container_width=True,
        height=min(400, (len(table3) + 1) * 38 + 10)
    )
else:
    st.success("✅ कोणतेही डुप्लिकेट सहभागी आढळले नाहीत.")

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# FOOTER
# =====================
st.markdown("""
<hr/>
<div style="text-align:center; color:rgba(255,255,255,0.7); font-size:13px; padding: 8px 0 16px 0;">
    🌸 आशा मॉनिटरिंग डॅशबोर्ड &nbsp;·&nbsp; KoboToolbox द्वारे &nbsp;·&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)
