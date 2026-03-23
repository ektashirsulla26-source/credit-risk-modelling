import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ── Page configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main { background-color: #f8f9fc; }

    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        color: #1a2744;
        margin-bottom: 0.2rem;
        line-height: 1.1;
    }

    .hero-sub {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    .section-header {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.8rem;
        margin-top: 1.5rem;
    }

    .result-card {
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }

    .result-p1 { background: linear-gradient(135deg, #d1fae5, #a7f3d0); border: 2px solid #34d399; }
    .result-p2 { background: linear-gradient(135deg, #dbeafe, #bfdbfe); border: 2px solid #60a5fa; }
    .result-p3 { background: linear-gradient(135deg, #fef3c7, #fde68a); border: 2px solid #f59e0b; }
    .result-p4 { background: linear-gradient(135deg, #fee2e2, #fecaca); border: 2px solid #f87171; }

    .result-tier {
        font-family: 'DM Serif Display', serif;
        font-size: 4rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .result-label {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    .result-action {
        font-size: 0.9rem;
        color: #374151;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.6);
        border-radius: 8px;
        display: inline-block;
        margin-top: 0.5rem;
    }

    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    .metric-val {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a2744;
    }

    .metric-lbl {
        font-size: 0.75rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .prob-bar-container {
        background: #f3f4f6;
        border-radius: 8px;
        height: 10px;
        margin: 4px 0;
        overflow: hidden;
    }

    .stButton > button {
        background: #1a2744;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2.5rem;
        font-size: 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background: #2d3f6e;
        transform: translateY(-1px);
    }

    .sidebar-info {
        background: #f0f4ff;
        border-radius: 10px;
        padding: 1rem;
        font-size: 0.85rem;
        color: #374151;
        border-left: 3px solid #4f73df;
    }

    .feature-tag {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.75rem;
        margin: 2px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ── Load model ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_pipeline():
    model_path = "xgboost_credit_pipeline.pkl"
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)


bundle = load_pipeline()

# ── Tier configuration ───────────────────────────────────────────────────────
TIER_CONFIG = {
    'P1': {
        'label':       'Very Low Risk',
        'action':      'Approve — offer best interest rate',
        'description': 'Excellent credit history. Strong repayment behaviour with no recent delinquencies.',
        'color':       'result-p1',
        'emoji':       '✅',
        'text_color':  '#065f46'
    },
    'P2': {
        'label':       'Low-Moderate Risk',
        'action':      'Approve — standard interest rate',
        'description': 'Good credit history with minor concerns. Suitable for standard loan products.',
        'color':       'result-p2',
        'emoji':       '🔵',
        'text_color':  '#1e40af'
    },
    'P3': {
        'label':       'Moderate-High Risk',
        'action':      'Conditional — review required',
        'description': 'Some delinquency history detected. Recommend closer review before approval.',
        'color':       'result-p3',
        'emoji':       '⚠️',
        'text_color':  '#92400e'
    },
    'P4': {
        'label':       'High Risk',
        'action':      'Reject — high risk applicant',
        'description': 'Significant delinquency or default history. High probability of repayment failure.',
        'color':       'result-p4',
        'emoji':       '🚫',
        'text_color':  '#991b1b'
    }
}

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 Credit Risk Tool")
    st.markdown("---")

    st.markdown("""
    <div class="sidebar-info">
    This tool uses a trained <b>XGBoost classifier</b> to assess credit risk
    and classify applicants into four risk tiers based on their credit bureau profile.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Risk Tiers")
    tier_descriptions = [
        ("P1", "✅", "#d1fae5", "Very Low Risk"),
        ("P2", "🔵", "#dbeafe", "Low-Moderate Risk"),
        ("P3", "⚠️", "#fef3c7", "Moderate-High Risk"),
        ("P4", "🚫", "#fee2e2", "High Risk"),
    ]
    for tier, emoji, color, label in tier_descriptions:
        st.markdown(
            f'<div style="background:{color};border-radius:8px;padding:6px 10px;'
            f'margin:4px 0;font-size:0.85rem;">'
            f'<b>{tier}</b> {emoji} — {label}</div>',
            unsafe_allow_html=True
        )

    st.markdown("### Model Info")
    st.markdown("""
    - **Algorithm**: XGBoost
    - **Features**: 54 credit bureau variables
    - **Training data**: 42,064 customers
    - **Validation**: 5-Fold Cross Validation
    - **CV Accuracy**: 78.09%
    - **CV Macro F1**: 0.6864
    """)

    if bundle is None:
        st.error("⚠️ Model file not found!\nPlace `xgboost_credit_pipeline.pkl` in the app folder.")
    else:
        st.success("✅ Model loaded successfully")


# ── Main content ─────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Credit Risk Assessment</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Enter applicant details below to receive an instant risk tier classification</div>', unsafe_allow_html=True)

if bundle is None:
    st.error("Model pipeline not loaded. Please ensure `xgboost_credit_pipeline.pkl` is in the same folder as `app.py`.")
    st.stop()

# ── Input form ───────────────────────────────────────────────────────────────
with st.form("credit_form"):

    # ── Section 1: Personal Information ─────────────────────────────────────
    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    with col2:
        education = st.selectbox("Education Level", [
            "SSC", "12TH", "GRADUATE", "UNDER GRADUATE",
            "POST-GRADUATE", "PROFESSIONAL", "OTHERS"
        ])
    with col3:
        gender = st.selectbox("Gender", ["M", "F"])

    col4, col5 = st.columns(2)
    with col4:
        net_monthly_income = st.number_input(
            "Net Monthly Income (₹)", min_value=0,
            max_value=10000000, value=50000, step=1000
        )
    with col5:
        time_with_curr_empr = st.number_input(
            "Time with Current Employer (months)",
            min_value=0, max_value=600, value=24
        )

    # ── Section 2: Trade Line History ────────────────────────────────────────
    st.markdown('<div class="section-header">Trade Line History</div>', unsafe_allow_html=True)
    col6, col7, col8 = st.columns(3)

    with col6:
        age_oldest_tl = st.number_input(
            "Age of Oldest Trade Line (months)",
            min_value=0, max_value=600, value=60
        )
    with col7:
        age_newest_tl = st.number_input(
            "Age of Newest Trade Line (months)",
            min_value=0, max_value=600, value=12
        )
    with col8:
        tot_tl_closed_l12m = st.number_input(
            "Trade Lines Closed in Last 12M",
            min_value=0, max_value=50, value=0
        )

    col9, col10, col11 = st.columns(3)
    with col9:
        cc_tl = st.number_input("Credit Card Trade Lines", min_value=0, max_value=20, value=1)
    with col10:
        home_tl = st.number_input("Home Loan Trade Lines", min_value=0, max_value=10, value=0)
    with col11:
        pl_tl = st.number_input("Personal Loan Trade Lines", min_value=0, max_value=20, value=1)

    col12, col13, col14 = st.columns(3)
    with col12:
        secured_tl = st.number_input("Secured Trade Lines", min_value=0, max_value=20, value=1)
    with col13:
        unsecured_tl = st.number_input("Unsecured Trade Lines", min_value=0, max_value=20, value=2)
    with col14:
        other_tl = st.number_input("Other Trade Lines", min_value=0, max_value=20, value=0)

    # ── Section 3: Payment & Delinquency ─────────────────────────────────────
    st.markdown('<div class="section-header">Payment & Delinquency History</div>', unsafe_allow_html=True)
    col15, col16, col17 = st.columns(3)

    with col15:
        time_since_recent_payment = st.number_input(
            "Time Since Recent Payment (months)",
            min_value=0, max_value=120, value=2
        )
    with col16:
        max_recent_level_of_deliq = st.number_input(
            "Max Recent Level of Delinquency",
            min_value=0, max_value=10, value=0
        )
    with col17:
        recent_level_of_deliq = st.number_input(
            "Recent Level of Delinquency",
            min_value=0, max_value=10, value=0
        )

    col18, col19, col20 = st.columns(3)
    with col18:
        tot_missed_pmnt = st.number_input("Total Missed Payments", min_value=0, max_value=50, value=0)
    with col19:
        num_deliq_6_12mts = st.number_input("Delinquencies (6-12 months)", min_value=0, max_value=20, value=0)
    with col20:
        num_times_60p_dpd = st.number_input("Times 60+ DPD", min_value=0, max_value=20, value=0)

    col21, col22, col23 = st.columns(3)
    with col21:
        num_std_12mts = st.number_input("Standard Accounts Last 12M", min_value=0, max_value=20, value=2)
    with col22:
        num_sub = st.number_input("Substandard Accounts", min_value=0, max_value=20, value=0)
    with col23:
        num_sub_6mts = st.number_input("Substandard Accounts (6M)", min_value=0, max_value=20, value=0)

    col24, col25, col26 = st.columns(3)
    with col24:
        num_sub_12mts = st.number_input("Substandard Accounts (12M)", min_value=0, max_value=20, value=0)
    with col25:
        num_dbt = st.number_input("Doubtful Accounts", min_value=0, max_value=20, value=0)
    with col26:
        num_dbt_12mts = st.number_input("Doubtful Accounts (12M)", min_value=0, max_value=20, value=0)

    col27, col28 = st.columns(2)
    with col27:
        num_lss = st.number_input("Loss Accounts", min_value=0, max_value=20, value=0)

    # ── Section 4: Enquiry Information ───────────────────────────────────────
    st.markdown('<div class="section-header">Credit Enquiry History</div>', unsafe_allow_html=True)
    col29, col30, col31 = st.columns(3)

    with col29:
        time_since_recent_enq = st.number_input(
            "Time Since Recent Enquiry (months)",
            min_value=0, max_value=120, value=3
        )
    with col30:
        enq_l3m = st.number_input("Enquiries in Last 3 Months", min_value=0, max_value=20, value=1)
    with col31:
        cc_enq_l12m = st.number_input("CC Enquiries Last 12M", min_value=0, max_value=20, value=0)

    col32, col33 = st.columns(2)
    with col32:
        pl_enq_l12m = st.number_input("PL Enquiries Last 12M", min_value=0, max_value=20, value=1)

    # ── Section 5: Percentage & Flag Features ────────────────────────────────
    st.markdown('<div class="section-header">Percentage & Flag Features</div>', unsafe_allow_html=True)
    col34, col35 = st.columns(2)

    with col34:
        pct_tl_open_l6m = st.slider("% Trade Lines Opened L6M", 0.0, 1.0, 0.2, 0.01)
        pct_tl_closed_l6m = st.slider("% Trade Lines Closed L6M", 0.0, 1.0, 0.1, 0.01)
        pct_tl_closed_l12m = st.slider("% Trade Lines Closed L12M", 0.0, 1.0, 0.15, 0.01)
        pct_pl_enq_l6m_of_ever = st.slider("% PL Enquiries L6M of Ever", 0.0, 1.0, 0.3, 0.01)
        pct_cc_enq_l6m_of_ever = st.slider("% CC Enquiries L6M of Ever", 0.0, 1.0, 0.2, 0.01)

    with col35:
        cc_flag = st.selectbox("Has Credit Card (CC Flag)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        pl_flag = st.selectbox("Has Personal Loan (PL Flag)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        hl_flag = st.selectbox("Has Home Loan (HL Flag)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        gl_flag = st.selectbox("Has Gold Loan (GL Flag)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    # ── Section 6: Product Enquiry Type ──────────────────────────────────────
    st.markdown('<div class="section-header">Product Enquiry Type</div>', unsafe_allow_html=True)
    col36, col37 = st.columns(2)

    with col36:
        last_prod_enq2 = st.selectbox(
            "Last Product Enquiry",
            ["ConsumerLoan", "PL", "AL", "CC", "HL", "others"]
        )
    with col37:
        first_prod_enq2 = st.selectbox(
            "First Product Enquiry",
            ["ConsumerLoan", "PL", "AL", "CC", "HL", "others"]
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍 Assess Credit Risk")


# ── Prediction ───────────────────────────────────────────────────────────────
if submitted:

    # Map education to ordinal
    edu_map = {
        'SSC': 1, '12TH': 2, 'GRADUATE': 3,
        'UNDER GRADUATE': 3, 'PROFESSIONAL': 3,
        'POST-GRADUATE': 4, 'OTHERS': 1
    }

    # Build base feature dict with all numeric features
    base_features = {
        'pct_tl_open_L6M':           pct_tl_open_l6m,
        'pct_tl_closed_L6M':         pct_tl_closed_l6m,
        'Tot_TL_closed_L12M':        tot_tl_closed_l12m,
        'pct_tl_closed_L12M':        pct_tl_closed_l12m,
        'Tot_Missed_Pmnt':           tot_missed_pmnt,
        'CC_TL':                     cc_tl,
        'Home_TL':                   home_tl,
        'PL_TL':                     pl_tl,
        'Secured_TL':                secured_tl,
        'Unsecured_TL':              unsecured_tl,
        'Other_TL':                  other_tl,
        'Age_Oldest_TL':             age_oldest_tl,
        'Age_Newest_TL':             age_newest_tl,
        'time_since_recent_payment': time_since_recent_payment,
        'max_recent_level_of_deliq': max_recent_level_of_deliq,
        'num_deliq_6_12mts':         num_deliq_6_12mts,
        'num_times_60p_dpd':         num_times_60p_dpd,
        'num_std_12mts':             num_std_12mts,
        'num_sub':                   num_sub,
        'num_sub_6mts':              num_sub_6mts,
        'num_sub_12mts':             num_sub_12mts,
        'num_dbt':                   num_dbt,
        'num_dbt_12mts':             num_dbt_12mts,
        'num_lss':                   num_lss,
        'recent_level_of_deliq':     recent_level_of_deliq,
        'CC_enq_L12m':               cc_enq_l12m,
        'PL_enq_L12m':               pl_enq_l12m,
        'time_since_recent_enq':     time_since_recent_enq,
        'enq_L3m':                   enq_l3m,
        'NETMONTHLYINCOME':          net_monthly_income,
        'Time_With_Curr_Empr':       time_with_curr_empr,
        'CC_Flag':                   cc_flag,
        'PL_Flag':                   pl_flag,
        'pct_PL_enq_L6m_of_ever':   pct_pl_enq_l6m_of_ever,
        'pct_CC_enq_L6m_of_ever':   pct_cc_enq_l6m_of_ever,
        'HL_Flag':                   hl_flag,
        'GL_Flag':                   gl_flag,
        'EDUCATION':                 edu_map[education],
        # One-hot: MARITALSTATUS
        'MARITALSTATUS_Married':     1 if marital_status == 'Married' else 0,
        'MARITALSTATUS_Single':      1 if marital_status == 'Single'  else 0,
        # One-hot: GENDER
        'GENDER_F':                  1 if gender == 'F' else 0,
        'GENDER_M':                  1 if gender == 'M' else 0,
        # One-hot: last_prod_enq2
        'last_prod_enq2_AL':           1 if last_prod_enq2 == 'AL'           else 0,
        'last_prod_enq2_CC':           1 if last_prod_enq2 == 'CC'           else 0,
        'last_prod_enq2_ConsumerLoan': 1 if last_prod_enq2 == 'ConsumerLoan' else 0,
        'last_prod_enq2_HL':           1 if last_prod_enq2 == 'HL'           else 0,
        'last_prod_enq2_PL':           1 if last_prod_enq2 == 'PL'           else 0,
        'last_prod_enq2_others':       1 if last_prod_enq2 == 'others'       else 0,
        # One-hot: first_prod_enq2
        'first_prod_enq2_AL':          1 if first_prod_enq2 == 'AL'           else 0,
        'first_prod_enq2_CC':          1 if first_prod_enq2 == 'CC'           else 0,
        'first_prod_enq2_ConsumerLoan':1 if first_prod_enq2 == 'ConsumerLoan' else 0,
        'first_prod_enq2_HL':          1 if first_prod_enq2 == 'HL'           else 0,
        'first_prod_enq2_PL':          1 if first_prod_enq2 == 'PL'           else 0,
        'first_prod_enq2_others':      1 if first_prod_enq2 == 'others'       else 0,
    }

    # Build DataFrame in correct feature order
    feature_names = bundle['feature_names']
    input_df = pd.DataFrame([base_features])[feature_names]

    # Apply scaling
    for col in bundle['scaled_cols']:
        if col in input_df.columns:
            input_df[col] = bundle['scalers'][col].transform(input_df[[col]])

    # Predict class and probabilities
    pred_encoded = bundle['model'].predict(input_df)[0]
    pred_tier    = bundle['label_encoder'].inverse_transform([pred_encoded])[0]

    # Get probabilities using predict_proba
    try:
        proba = bundle['model'].predict_proba(input_df)[0]
    except Exception:
        proba = None

    cfg = TIER_CONFIG[pred_tier]

    # ── Results display ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Assessment Result")

    col_res, col_detail = st.columns([1, 1.5])

    with col_res:
        st.markdown(f"""
        <div class="result-card {cfg['color']}">
            <div class="result-tier" style="color:{cfg['text_color']}">
                {pred_tier}
            </div>
            <div class="result-label" style="color:{cfg['text_color']}">
                {cfg['emoji']} {cfg['label']}
            </div>
            <div class="result-action">{cfg['action']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_detail:
        st.markdown("#### Risk Assessment Details")
        st.info(cfg['description'])

        if proba is not None:
            st.markdown("#### Probability Breakdown")
            classes = bundle['label_encoder'].classes_
            colors  = {'P1': '#34d399', 'P2': '#60a5fa',
                       'P3': '#f59e0b', 'P4': '#f87171'}

            for i, cls in enumerate(classes):
                pct = proba[i] * 100
                bar_color = colors.get(cls, '#9ca3af')
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="width:28px;font-weight:600;font-size:0.85rem">{cls}</span>
                    <div style="flex:1;background:#f3f4f6;border-radius:8px;height:14px;overflow:hidden;">
                        <div style="width:{pct:.1f}%;background:{bar_color};
                                    height:100%;border-radius:8px;
                                    transition:width 0.5s ease;"></div>
                    </div>
                    <span style="width:45px;text-align:right;font-size:0.85rem;
                                 color:#374151;">{pct:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)

    # ── Key risk indicators ───────────────────────────────────────────────────
    st.markdown("#### Key Input Summary")
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{age_oldest_tl}</div>
            <div class="metric-lbl">Oldest TL (mo)</div>
        </div>""", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{enq_l3m}</div>
            <div class="metric-lbl">Enquiries L3M</div>
        </div>""", unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{max_recent_level_of_deliq}</div>
            <div class="metric-lbl">Max Delinquency</div>
        </div>""", unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">₹{net_monthly_income:,}</div>
            <div class="metric-lbl">Monthly Income</div>
        </div>""", unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{num_std_12mts}</div>
            <div class="metric-lbl">Std Accounts 12M</div>
        </div>""", unsafe_allow_html=True)

    # ── Expandable raw input ──────────────────────────────────────────────────
    with st.expander("📋 View full input data sent to model"):
        st.dataframe(
            pd.DataFrame([base_features]).T.rename(columns={0: 'Value'}),
            use_container_width=True
        )