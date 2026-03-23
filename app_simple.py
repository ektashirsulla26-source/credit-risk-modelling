import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.hero { text-align:center; padding: 2rem 0 1rem 0; }
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem; color: #1a2744; line-height:1.1;
}
.hero-sub { font-size:1rem; color:#6b7280; margin-top:0.5rem; }

.step-label {
    font-size:0.7rem; font-weight:600; letter-spacing:0.12em;
    text-transform:uppercase; color:#9ca3af;
    margin-bottom:0.5rem; margin-top:1.5rem;
}

.result-card {
    border-radius:16px; padding:2rem;
    text-align:center; margin:1.5rem 0;
}
.result-p1 { background:linear-gradient(135deg,#d1fae5,#a7f3d0); border:2px solid #34d399; }
.result-p2 { background:linear-gradient(135deg,#dbeafe,#bfdbfe); border:2px solid #60a5fa; }
.result-p3 { background:linear-gradient(135deg,#fef3c7,#fde68a); border:2px solid #f59e0b; }
.result-p4 { background:linear-gradient(135deg,#fee2e2,#fecaca); border:2px solid #f87171; }

.result-tier {
    font-family:'DM Serif Display',serif;
    font-size:4.5rem; font-weight:700; line-height:1; margin-bottom:0.4rem;
}
.result-label { font-size:1.2rem; font-weight:600; margin-bottom:0.4rem; }
.result-action {
    font-size:0.95rem; color:#374151;
    padding:0.5rem 1.2rem;
    background:rgba(255,255,255,0.65);
    border-radius:8px; display:inline-block; margin-top:0.5rem;
}

.tip-box {
    background:#f0f9ff; border-left:4px solid #38bdf8;
    border-radius:0 8px 8px 0; padding:0.8rem 1rem;
    font-size:0.85rem; color:#0369a1; margin:0.5rem 0;
}

.stButton > button {
    background:#1a2744; color:white; border:none;
    border-radius:10px; padding:0.8rem 2rem;
    font-size:1rem; font-weight:500; width:100%;
}
.stButton > button:hover { background:#2d3f6e; }
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_pipeline():
    if not os.path.exists("xgboost_credit_pipeline.pkl"):
        return None
    return joblib.load("xgboost_credit_pipeline.pkl")

bundle = load_pipeline()

TIER_CONFIG = {
    'P1': {'label':'Very Low Risk',      'action':'Approve — best interest rate',
           'color':'result-p1',          'emoji':'✅', 'text_color':'#065f46',
           'desc':'Excellent credit profile. Strong repayment history.'},
    'P2': {'label':'Low-Moderate Risk',  'action':'Approve — standard interest rate',
           'color':'result-p2',          'emoji':'🔵', 'text_color':'#1e40af',
           'desc':'Good credit profile with minor concerns.'},
    'P3': {'label':'Moderate-High Risk', 'action':'Conditional — review required',
           'color':'result-p3',          'emoji':'⚠️', 'text_color':'#92400e',
           'desc':'Some payment issues detected. Closer review recommended.'},
    'P4': {'label':'High Risk',          'action':'Reject — high risk applicant',
           'color':'result-p4',          'emoji':'🚫', 'text_color':'#991b1b',
           'desc':'Significant repayment risk. High chance of default.'},
}

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🏦 Credit Risk Assessment</div>
    <div class="hero-sub">Answer a few simple questions to get an instant loan risk assessment</div>
</div>
""", unsafe_allow_html=True)

if bundle is None:
    st.error("Model file not found. Please ensure `xgboost_credit_pipeline.pkl` is in the same folder.")
    st.stop()

# ── Simple form ───────────────────────────────────────────────────────────────
with st.form("simple_form"):

    # ── Personal ─────────────────────────────────────────────────────────────
    st.markdown('<div class="step-label">👤 About You</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        marital_status = st.selectbox("Marital Status", ["Married", "Single"])
    with col2:
        education = st.selectbox("Highest Education", [
            "Below 10th (SSC)", "12th Pass", "Graduate",
            "Under Graduate", "Post Graduate", "Professional", "Others"
        ])
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female"])

    col4, col5 = st.columns(2)
    with col4:
        monthly_income = st.number_input(
            "Monthly Income (₹)", min_value=0,
            max_value=10000000, value=50000, step=5000,
            help="Your take-home salary per month"
        )
    with col5:
        job_tenure = st.number_input(
            "How long at current job? (months)",
            min_value=0, max_value=600, value=24,
            help="Number of months with your current employer"
        )

    # ── Loan history ─────────────────────────────────────────────────────────
    st.markdown('<div class="step-label">💳 Your Loan & Credit History</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 These questions are about all loans/credit cards you have ever taken</div>',
                unsafe_allow_html=True)

    col6, col7 = st.columns(2)
    with col6:
        credit_age = st.number_input(
            "How old is your oldest loan/credit card? (months)",
            min_value=0, max_value=600, value=60,
            help="e.g. if you took a loan 5 years ago, enter 60"
        )
        has_credit_card = st.selectbox("Do you have a Credit Card?",
                                       ["Yes", "No"])
        has_home_loan   = st.selectbox("Do you have a Home Loan?",
                                       ["No", "Yes"])

    with col7:
        has_personal_loan = st.selectbox("Do you have a Personal Loan?",
                                         ["No", "Yes"])
        has_gold_loan     = st.selectbox("Do you have a Gold Loan?",
                                         ["No", "Yes"])
        last_product      = st.selectbox("What type of loan are you applying for?", [
            "Personal Loan", "Consumer Loan", "Auto Loan",
            "Credit Card", "Home Loan", "Others"
        ])

    # ── Payment behaviour ─────────────────────────────────────────────────────
    st.markdown('<div class="step-label">📅 Payment Behaviour</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="tip-box">💡 Be honest — this helps assess your actual risk accurately</div>',
                unsafe_allow_html=True)

    col8, col9 = st.columns(2)
    with col8:
        missed_payments = st.selectbox(
            "Have you ever missed a loan payment?",
            ["Never", "1-2 times", "3-5 times", "More than 5 times"]
        )
        recent_payment_months = st.number_input(
            "How many months since your last payment?",
            min_value=0, max_value=120, value=1,
            help="Enter 0 if you paid this month"
        )
    with col9:
        recent_enquiries = st.number_input(
            "How many loan applications in last 3 months?",
            min_value=0, max_value=20, value=1,
            help="Count all banks/NBFCs you applied to recently"
        )
        delinquency_level = st.selectbox(
            "Any overdue payments currently?",
            ["No overdue", "Slightly overdue (1-30 days)",
             "Moderately overdue (30-90 days)", "Severely overdue (90+ days)"]
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍  Check My Credit Risk")


# ── Convert simple inputs to model features ───────────────────────────────────
if submitted:

    # Education mapping
    edu_map = {
        "Below 10th (SSC)": 1, "12th Pass": 2, "Graduate": 3,
        "Under Graduate": 3,   "Professional": 3,
        "Post Graduate": 4,    "Others": 1
    }

    # Missed payments → numeric
    missed_map = {
        "Never": 0, "1-2 times": 1,
        "3-5 times": 3, "More than 5 times": 6
    }

    # Delinquency → level
    deliq_map = {
        "No overdue": 0,
        "Slightly overdue (1-30 days)": 1,
        "Moderately overdue (30-90 days)": 3,
        "Severely overdue (90+ days)": 6
    }

    # Product mapping
    prod_map = {
        "Personal Loan": "PL",    "Consumer Loan": "ConsumerLoan",
        "Auto Loan": "AL",        "Credit Card": "CC",
        "Home Loan": "HL",        "Others": "others"
    }

    g       = "M" if gender == "Male" else "F"
    cc_flag = 1 if has_credit_card   == "Yes" else 0
    pl_flag = 1 if has_personal_loan == "Yes" else 0
    hl_flag = 1 if has_home_loan     == "Yes" else 0
    gl_flag = 1 if has_gold_loan     == "Yes" else 0
    deliq   = deliq_map[delinquency_level]
    missed  = missed_map[missed_payments]
    lp      = prod_map[last_product]

    # Build full feature dict with sensible defaults for fields not asked
    base_features = {
        'pct_tl_open_L6M':             0.15,
        'pct_tl_closed_L6M':           0.10,
        'Tot_TL_closed_L12M':          0,
        'pct_tl_closed_L12M':          0.10,
        'Tot_Missed_Pmnt':             missed,
        'CC_TL':                       cc_flag,
        'Home_TL':                     hl_flag,
        'PL_TL':                       pl_flag,
        'Secured_TL':                  hl_flag + gl_flag,
        'Unsecured_TL':                cc_flag + pl_flag,
        'Other_TL':                    0,
        'Age_Oldest_TL':               credit_age,
        'Age_Newest_TL':               min(12, credit_age),
        'time_since_recent_payment':   recent_payment_months,
        'max_recent_level_of_deliq':   deliq,
        'num_deliq_6_12mts':           1 if deliq > 0 else 0,
        'num_times_60p_dpd':           1 if deliq >= 3 else 0,
        'num_std_12mts':               2,
        'num_sub':                     1 if deliq > 0 else 0,
        'num_sub_6mts':                1 if deliq > 0 else 0,
        'num_sub_12mts':               1 if deliq > 0 else 0,
        'num_dbt':                     1 if deliq >= 3 else 0,
        'num_dbt_12mts':               1 if deliq >= 3 else 0,
        'num_lss':                     1 if deliq >= 6 else 0,
        'recent_level_of_deliq':       deliq,
        'CC_enq_L12m':                 recent_enquiries if lp == 'CC' else 0,
        'PL_enq_L12m':                 recent_enquiries if lp == 'PL' else 0,
        'time_since_recent_enq':       1,
        'enq_L3m':                     recent_enquiries,
        'NETMONTHLYINCOME':            monthly_income,
        'Time_With_Curr_Empr':         job_tenure,
        'CC_Flag':                     cc_flag,
        'PL_Flag':                     pl_flag,
        'pct_PL_enq_L6m_of_ever':     0.3 if lp == 'PL' else 0.1,
        'pct_CC_enq_L6m_of_ever':     0.3 if lp == 'CC' else 0.1,
        'HL_Flag':                     hl_flag,
        'GL_Flag':                     gl_flag,
        'EDUCATION':                   edu_map[education],
        'MARITALSTATUS_Married':       1 if marital_status == 'Married' else 0,
        'MARITALSTATUS_Single':        1 if marital_status == 'Single'  else 0,
        'GENDER_F':                    1 if g == 'F' else 0,
        'GENDER_M':                    1 if g == 'M' else 0,
        'last_prod_enq2_AL':           1 if lp == 'AL'           else 0,
        'last_prod_enq2_CC':           1 if lp == 'CC'           else 0,
        'last_prod_enq2_ConsumerLoan': 1 if lp == 'ConsumerLoan' else 0,
        'last_prod_enq2_HL':           1 if lp == 'HL'           else 0,
        'last_prod_enq2_PL':           1 if lp == 'PL'           else 0,
        'last_prod_enq2_others':       1 if lp == 'others'       else 0,
        'first_prod_enq2_AL':          0,
        'first_prod_enq2_CC':          1 if lp == 'CC' else 0,
        'first_prod_enq2_ConsumerLoan':1 if lp == 'ConsumerLoan' else 0,
        'first_prod_enq2_HL':          0,
        'first_prod_enq2_PL':          1 if lp == 'PL' else 0,
        'first_prod_enq2_others':      0 if lp in ['CC','PL','ConsumerLoan'] else 1,
    }

    feature_names = bundle['feature_names']
    input_df = pd.DataFrame([base_features])[feature_names]

    for col in bundle['scaled_cols']:
        if col in input_df.columns:
            input_df[col] = bundle['scalers'][col].transform(input_df[[col]])

    pred_encoded = bundle['model'].predict(input_df)[0]
    pred_tier    = bundle['label_encoder'].inverse_transform([pred_encoded])[0]

    try:
        proba = bundle['model'].predict_proba(input_df)[0]
    except Exception:
        proba = None

    cfg = TIER_CONFIG[pred_tier]

    # ── Result display ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## Your Assessment Result")

    col_r, col_d = st.columns([1, 1.4])

    with col_r:
        st.markdown(f"""
        <div class="result-card {cfg['color']}">
            <div class="result-tier" style="color:{cfg['text_color']}">{pred_tier}</div>
            <div class="result-label" style="color:{cfg['text_color']}">{cfg['emoji']} {cfg['label']}</div>
            <div class="result-action">{cfg['action']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_d:
        st.markdown("#### What this means")
        st.info(cfg['desc'])

        if proba is not None:
            st.markdown("#### Confidence breakdown")
            classes = bundle['label_encoder'].classes_
            colors  = {'P1':'#34d399','P2':'#60a5fa',
                       'P3':'#f59e0b','P4':'#f87171'}
            for i, cls in enumerate(classes):
                pct = proba[i] * 100
                bc  = colors.get(cls, '#9ca3af')
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="width:28px;font-weight:600;font-size:0.85rem">{cls}</span>
                    <div style="flex:1;background:#f3f4f6;border-radius:8px;height:14px;overflow:hidden;">
                        <div style="width:{pct:.1f}%;background:{bc};height:100%;border-radius:8px;"></div>
                    </div>
                    <span style="width:45px;text-align:right;font-size:0.85rem;color:#374151;">{pct:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)

    # ── What to do next ────────────────────────────────────────────────────────
    st.markdown("#### What should you do next?")
    next_steps = {
        'P1': [
            "✅ You qualify for the best loan rates available",
            "✅ Apply confidently — your profile is strong",
            "✅ Consider negotiating for lower interest rates"
        ],
        'P2': [
            "✅ You are likely to get loan approval",
            "💡 Compare rates across multiple banks before applying",
            "💡 Maintaining timely payments will move you to P1"
        ],
        'P3': [
            "⚠️ Your application may need additional review",
            "💡 Clear any overdue payments before applying",
            "💡 Reduce recent loan enquiries — too many hurt your score",
            "💡 Wait 3–6 months and re-apply after improving payment history"
        ],
        'P4': [
            "🚫 A loan approval is unlikely at this stage",
            "💡 Clear all overdue amounts immediately",
            "💡 Do not apply for any new loans for at least 6 months",
            "💡 Consider a secured loan (against FD/gold) as an alternative",
            "💡 Check your CIBIL report for any errors"
        ]
    }
    for step in next_steps[pred_tier]:
        st.markdown(f"- {step}")

    st.markdown("---")
    st.caption("⚠️ This assessment is for informational purposes only and is based on a machine learning model. Final loan decisions are made by the lending institution.")