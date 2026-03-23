import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem; color: #1a2744; line-height:1.1; margin-bottom:0.2rem;
}
.hero-sub { font-size:1rem; color:#6b7280; margin-bottom:1.5rem; }

.mode-badge-simple {
    display:inline-block; background:#dbeafe; color:#1e40af;
    border-radius:20px; padding:4px 14px; font-size:0.8rem;
    font-weight:600; margin-bottom:1rem;
}
.mode-badge-expert {
    display:inline-block; background:#fef3c7; color:#92400e;
    border-radius:20px; padding:4px 14px; font-size:0.8rem;
    font-weight:600; margin-bottom:1rem;
}

.section-header {
    font-size:0.72rem; font-weight:600; letter-spacing:0.12em;
    text-transform:uppercase; color:#9ca3af;
    margin-bottom:0.6rem; margin-top:1.4rem;
}

.result-card {
    border-radius:16px; padding:2rem;
    text-align:center; margin:1rem 0;
}
.result-p1 { background:linear-gradient(135deg,#d1fae5,#a7f3d0); border:2px solid #34d399; }
.result-p2 { background:linear-gradient(135deg,#dbeafe,#bfdbfe); border:2px solid #60a5fa; }
.result-p3 { background:linear-gradient(135deg,#fef3c7,#fde68a); border:2px solid #f59e0b; }
.result-p4 { background:linear-gradient(135deg,#fee2e2,#fecaca); border:2px solid #f87171; }

.result-tier {
    font-family:'DM Serif Display',serif;
    font-size:4.5rem; font-weight:700; line-height:1; margin-bottom:0.4rem;
}
.result-label  { font-size:1.2rem; font-weight:600; margin-bottom:0.4rem; }
.result-action {
    font-size:0.95rem; color:#374151;
    padding:0.5rem 1.2rem;
    background:rgba(255,255,255,0.65);
    border-radius:8px; display:inline-block; margin-top:0.5rem;
}

.metric-box {
    background:white; border-radius:12px;
    padding:1rem 1.2rem; border:1px solid #e5e7eb; text-align:center;
}
.metric-val { font-size:1.6rem; font-weight:600; color:#1a2744; }
.metric-lbl { font-size:0.72rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.05em; }

.tip-box {
    background:#f0f9ff; border-left:4px solid #38bdf8;
    border-radius:0 8px 8px 0; padding:0.8rem 1rem;
    font-size:0.85rem; color:#0369a1; margin:0.5rem 0;
}

.disclaimer-box {
    background:#f8f9fc; border:1px solid #e5e7eb;
    border-radius:10px; padding:1rem 1.2rem;
    font-size:0.78rem; color:#6b7280;
    line-height:1.6; margin-top:1.5rem;
}

.github-btn {
    display:inline-block;
    background:#24292e; color:white !important;
    border-radius:8px; padding:8px 16px;
    font-size:0.85rem; font-weight:500;
    text-decoration:none; margin-top:0.5rem;
}
.github-btn:hover { background:#3d444d; }

.sidebar-section {
    background:#f8f9fc; border-radius:10px;
    padding:0.8rem 1rem; margin:0.5rem 0;
    font-size:0.83rem; color:#374151;
}

.stButton > button {
    background:#1a2744; color:white; border:none;
    border-radius:10px; padding:0.8rem 2rem;
    font-size:1rem; font-weight:500; width:100%;
}
.stButton > button:hover { background:#2d3f6e; }

div[data-testid="stExpander"] {
    border:1px solid #e5e7eb; border-radius:12px; overflow:hidden;
}
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
           'desc':'Excellent credit profile. Strong repayment history with no delinquencies.'},
    'P2': {'label':'Low-Moderate Risk',  'action':'Approve — standard interest rate',
           'color':'result-p2',          'emoji':'🔵', 'text_color':'#1e40af',
           'desc':'Good credit profile with minor concerns. Suitable for standard loan products.'},
    'P3': {'label':'Moderate-High Risk', 'action':'Conditional — review required',
           'color':'result-p3',          'emoji':'⚠️', 'text_color':'#92400e',
           'desc':'Some delinquency history detected. Recommend closer review before approval.'},
    'P4': {'label':'High Risk',          'action':'Reject — high risk applicant',
           'color':'result-p4',          'emoji':'🚫', 'text_color':'#991b1b',
           'desc':'Significant delinquency or default history. High probability of repayment failure.'},
}

NEXT_STEPS = {
    'P1': ["✅ You qualify for the best loan rates available",
           "✅ Apply confidently — your credit profile is strong",
           "✅ Consider negotiating for lower interest rates"],
    'P2': ["✅ You are likely to get loan approval",
           "💡 Compare rates across multiple banks before applying",
           "💡 Maintaining timely payments will move you to P1 tier"],
    'P3': ["⚠️ Your application may need additional review",
           "💡 Clear any overdue payments before applying",
           "💡 Reduce recent loan enquiries — too many hurt your score",
           "💡 Wait 3–6 months and re-apply after improving payment history"],
    'P4': ["🚫 A loan approval is unlikely at this stage",
           "💡 Clear all overdue amounts immediately",
           "💡 Do not apply for any new loans for at least 6 months",
           "💡 Consider a secured loan (against FD/gold) as an alternative",
           "💡 Check your CIBIL report for any errors at www.cibil.com"],
}


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏦 Credit Risk Tool")
    st.markdown("---")

    # ── Mode toggle ───────────────────────────────────────────
    st.markdown("### 🔄 Select Mode")
    mode = st.radio(
        "",
        ["🟢 Simple Mode — Easy Questions",
         "🟡 Expert Mode — Full Technical Input"],
        index=0,
        help="Simple mode asks plain English questions. Expert mode takes raw credit bureau fields."
    )
    is_simple = "Simple" in mode
    st.markdown("---")

    # ── Risk tiers ────────────────────────────────────────────
    st.markdown("### Risk Tiers")
    for tier, bg, emoji, label in [
        ("P1","#d1fae5","✅","Very Low Risk"),
        ("P2","#dbeafe","🔵","Low-Moderate Risk"),
        ("P3","#fef3c7","⚠️","Moderate-High Risk"),
        ("P4","#fee2e2","🚫","High Risk"),
    ]:
        st.markdown(
            f'<div style="background:{bg};border-radius:8px;padding:6px 10px;'
            f'margin:4px 0;font-size:0.83rem;">'
            f'<b>{tier}</b> {emoji} — {label}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Model info ────────────────────────────────────────────
    st.markdown("### ⚙️ Model Info")
    st.markdown("""
    <div class="sidebar-section">
    <b>Algorithm</b>: XGBoost<br>
    <b>Features</b>: 54 credit bureau variables<br>
    <b>Training data</b>: 42,064 customers<br>
    <b>Validation</b>: 5-Fold Stratified CV<br>
    <b>CV Accuracy</b>: 78.09% ± 0.25%<br>
    <b>CV Macro F1</b>: 0.6864 ± 0.38%<br>
    <b>P3 Recall (tuned)</b>: 69.4%
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── GitHub link ───────────────────────────────────────────
    # ⚠️ REPLACE the URL below with your actual GitHub repo link
    st.markdown("### 👨‍💻 Project Code")
    st.markdown("""
    <div class="sidebar-section">
    View the full project source code, notebooks,
    and data pipeline on GitHub.
    </div>
    """, unsafe_allow_html=True)

    GITHUB_URL = "https://github.com/ektashirsulla26-source/credit_risk_modelling"
    st.markdown(
        f'<a href="{GITHUB_URL}" target="_blank" class="github-btn">'
        f'⭐ View on GitHub</a>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ── Model status ──────────────────────────────────────────
    if bundle is None:
        st.error("⚠️ Model file not found!")
    else:
        st.success("✅ Model loaded successfully")


# ═══════════════════════════════════════════════════════════════
# MAIN PAGE HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="hero-title">Credit Risk Assessment</div>',
            unsafe_allow_html=True)

if is_simple:
    st.markdown(
        '<span class="mode-badge-simple">🟢 Simple Mode — Plain English Questions</span>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="hero-sub">Answer a few simple questions to get an instant loan risk assessment</div>',
                unsafe_allow_html=True)
else:
    st.markdown(
        '<span class="mode-badge-expert">🟡 Expert Mode — Full Credit Bureau Input</span>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="hero-sub">Enter full credit bureau variables for a detailed technical assessment</div>',
                unsafe_allow_html=True)

if bundle is None:
    st.error("Model pipeline not loaded. Please ensure `xgboost_credit_pipeline.pkl` is in the same folder as `app.py`.")
    st.stop()


# ═══════════════════════════════════════════════════════════════
# HELPER: PREDICTION + RESULT DISPLAY
# ═══════════════════════════════════════════════════════════════
def run_prediction(base_features, key_metrics):
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

    st.markdown("---")
    st.markdown("## Assessment Result")

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
        st.markdown("#### Risk Assessment Details")
        st.info(cfg['desc'])

        if proba is not None:
            st.markdown("#### Probability Breakdown")
            classes = bundle['label_encoder'].classes_
            colors  = {'P1':'#34d399','P2':'#60a5fa',
                       'P3':'#f59e0b','P4':'#f87171'}
            for i, cls in enumerate(classes):
                pct = proba[i] * 100
                bc  = colors.get(cls, '#9ca3af')
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="width:28px;font-weight:600;font-size:0.85rem">{cls}</span>
                    <div style="flex:1;background:#f3f4f6;border-radius:8px;
                                height:14px;overflow:hidden;">
                        <div style="width:{pct:.1f}%;background:{bc};
                                    height:100%;border-radius:8px;"></div>
                    </div>
                    <span style="width:45px;text-align:right;
                                 font-size:0.85rem;color:#374151;">{pct:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)

    # Key metrics summary
    st.markdown("#### Key Input Summary")
    cols = st.columns(len(key_metrics))
    for i, (val, lbl) in enumerate(key_metrics):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{val}</div>
                <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # What to do next
    st.markdown("#### What should you do next?")
    for step in NEXT_STEPS[pred_tier]:
        st.markdown(f"- {step}")

    # Full input viewer
    with st.expander("📋 View full input data sent to model"):
        st.dataframe(
            pd.DataFrame([base_features]).T.rename(columns={0: 'Value'}),
            use_container_width=True
        )

    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
    <b>⚠️ Disclaimer:</b> This credit risk assessment is generated by a machine learning
    model trained on historical credit bureau data and is provided for
    <b>informational and educational purposes only</b>. It does not constitute
    financial advice and should not be used as the sole basis for any lending
    decision. Actual credit decisions are made by licensed financial institutions
    using their own proprietary models, policies, and regulatory requirements.
    Model accuracy: CV Accuracy 78.09%, Macro F1 0.6864 (5-fold cross validation).
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SIMPLE MODE FORM
# ═══════════════════════════════════════════════════════════════
if is_simple:

    with st.form("simple_form"):

        st.markdown('<div class="section-header">👤 About You</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            marital_status = st.selectbox("Marital Status", ["Married", "Single"])
        with c2:
            education = st.selectbox("Highest Education", [
                "Below 10th (SSC)", "12th Pass", "Graduate",
                "Under Graduate", "Post Graduate", "Professional", "Others"
            ])
        with c3:
            gender = st.selectbox("Gender", ["Male", "Female"])

        c4, c5 = st.columns(2)
        with c4:
            monthly_income = st.number_input(
                "Monthly Income (₹)", min_value=0,
                max_value=10000000, value=50000, step=5000,
                help="Your take-home salary per month"
            )
        with c5:
            job_tenure = st.number_input(
                "Months at current job",
                min_value=0, max_value=600, value=24,
                help="Number of months with your current employer"
            )

        st.markdown('<div class="section-header">💳 Your Loan & Credit History</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="tip-box">💡 Questions about all loans/credit cards you have ever taken</div>',
                    unsafe_allow_html=True)

        c6, c7 = st.columns(2)
        with c6:
            credit_age        = st.number_input(
                "Age of oldest loan/credit card (months)",
                min_value=0, max_value=600, value=60,
                help="e.g. loan taken 5 years ago = enter 60"
            )
            has_credit_card   = st.selectbox("Have a Credit Card?", ["Yes","No"])
            has_home_loan     = st.selectbox("Have a Home Loan?",    ["No","Yes"])
        with c7:
            has_personal_loan = st.selectbox("Have a Personal Loan?",["No","Yes"])
            has_gold_loan     = st.selectbox("Have a Gold Loan?",     ["No","Yes"])
            last_product      = st.selectbox("Loan type applying for?", [
                "Personal Loan","Consumer Loan","Auto Loan",
                "Credit Card","Home Loan","Others"
            ])

        st.markdown('<div class="section-header">📅 Payment Behaviour</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="tip-box">💡 Be honest — this helps assess your actual risk accurately</div>',
                    unsafe_allow_html=True)

        c8, c9 = st.columns(2)
        with c8:
            missed_payments = st.selectbox(
                "Ever missed a loan payment?",
                ["Never","1-2 times","3-5 times","More than 5 times"]
            )
            recent_payment_months = st.number_input(
                "Months since last payment?",
                min_value=0, max_value=120, value=1,
                help="Enter 0 if you paid this month"
            )
        with c9:
            recent_enquiries = st.number_input(
                "Loan applications in last 3 months?",
                min_value=0, max_value=20, value=1,
                help="Count all banks/NBFCs you applied to"
            )
            delinquency_level = st.selectbox(
                "Any overdue payments currently?",
                ["No overdue","Slightly overdue (1-30 days)",
                 "Moderately overdue (30-90 days)","Severely overdue (90+ days)"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted_simple = st.form_submit_button("🔍  Check My Credit Risk")

    if submitted_simple:
        edu_map    = {"Below 10th (SSC)":1,"12th Pass":2,"Graduate":3,
                      "Under Graduate":3,"Professional":3,"Post Graduate":4,"Others":1}
        missed_map = {"Never":0,"1-2 times":1,"3-5 times":3,"More than 5 times":6}
        deliq_map  = {"No overdue":0,"Slightly overdue (1-30 days)":1,
                      "Moderately overdue (30-90 days)":3,"Severely overdue (90+ days)":6}
        prod_map   = {"Personal Loan":"PL","Consumer Loan":"ConsumerLoan",
                      "Auto Loan":"AL","Credit Card":"CC","Home Loan":"HL","Others":"others"}

        g      = "M" if gender == "Male" else "F"
        cc_f   = 1 if has_credit_card   == "Yes" else 0
        pl_f   = 1 if has_personal_loan == "Yes" else 0
        hl_f   = 1 if has_home_loan     == "Yes" else 0
        gl_f   = 1 if has_gold_loan     == "Yes" else 0
        deliq  = deliq_map[delinquency_level]
        missed = missed_map[missed_payments]
        lp     = prod_map[last_product]

        base_features = {
            'pct_tl_open_L6M':0.15,'pct_tl_closed_L6M':0.10,
            'Tot_TL_closed_L12M':0,'pct_tl_closed_L12M':0.10,
            'Tot_Missed_Pmnt':missed,'CC_TL':cc_f,'Home_TL':hl_f,
            'PL_TL':pl_f,'Secured_TL':hl_f+gl_f,'Unsecured_TL':cc_f+pl_f,
            'Other_TL':0,'Age_Oldest_TL':credit_age,
            'Age_Newest_TL':min(12,credit_age),
            'time_since_recent_payment':recent_payment_months,
            'max_recent_level_of_deliq':deliq,
            'num_deliq_6_12mts':1 if deliq>0 else 0,
            'num_times_60p_dpd':1 if deliq>=3 else 0,
            'num_std_12mts':2,'num_sub':1 if deliq>0 else 0,
            'num_sub_6mts':1 if deliq>0 else 0,
            'num_sub_12mts':1 if deliq>0 else 0,
            'num_dbt':1 if deliq>=3 else 0,
            'num_dbt_12mts':1 if deliq>=3 else 0,
            'num_lss':1 if deliq>=6 else 0,
            'recent_level_of_deliq':deliq,
            'CC_enq_L12m':recent_enquiries if lp=='CC' else 0,
            'PL_enq_L12m':recent_enquiries if lp=='PL' else 0,
            'time_since_recent_enq':1,'enq_L3m':recent_enquiries,
            'NETMONTHLYINCOME':monthly_income,'Time_With_Curr_Empr':job_tenure,
            'CC_Flag':cc_f,'PL_Flag':pl_f,
            'pct_PL_enq_L6m_of_ever':0.3 if lp=='PL' else 0.1,
            'pct_CC_enq_L6m_of_ever':0.3 if lp=='CC' else 0.1,
            'HL_Flag':hl_f,'GL_Flag':gl_f,
            'EDUCATION':edu_map[education],
            'MARITALSTATUS_Married':1 if marital_status=='Married' else 0,
            'MARITALSTATUS_Single': 1 if marital_status=='Single'  else 0,
            'GENDER_F':1 if g=='F' else 0,'GENDER_M':1 if g=='M' else 0,
            'last_prod_enq2_AL':          1 if lp=='AL'           else 0,
            'last_prod_enq2_CC':          1 if lp=='CC'           else 0,
            'last_prod_enq2_ConsumerLoan':1 if lp=='ConsumerLoan' else 0,
            'last_prod_enq2_HL':          1 if lp=='HL'           else 0,
            'last_prod_enq2_PL':          1 if lp=='PL'           else 0,
            'last_prod_enq2_others':      1 if lp=='others'       else 0,
            'first_prod_enq2_AL':0,
            'first_prod_enq2_CC':          1 if lp=='CC' else 0,
            'first_prod_enq2_ConsumerLoan':1 if lp=='ConsumerLoan' else 0,
            'first_prod_enq2_HL':0,
            'first_prod_enq2_PL':          1 if lp=='PL' else 0,
            'first_prod_enq2_others':      0 if lp in ['CC','PL','ConsumerLoan'] else 1,
        }

        key_metrics = [
            (credit_age,       "Oldest TL (mo)"),
            (recent_enquiries, "Enquiries L3M"),
            (deliq,            "Delinquency"),
            (f"₹{monthly_income:,}", "Monthly Income"),
            (job_tenure,       "Job Tenure (mo)"),
        ]
        run_prediction(base_features, key_metrics)


# ═══════════════════════════════════════════════════════════════
# EXPERT MODE FORM
# ═══════════════════════════════════════════════════════════════
else:
    with st.form("expert_form"):

        st.markdown('<div class="section-header">Personal Information</div>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: marital_status = st.selectbox("Marital Status", ["Married","Single"])
        with c2:
            education = st.selectbox("Education", [
                "SSC","12TH","GRADUATE","UNDER GRADUATE",
                "POST-GRADUATE","PROFESSIONAL","OTHERS"
            ])
        with c3: gender = st.selectbox("Gender", ["M","F"])

        c4, c5 = st.columns(2)
        with c4: net_monthly_income = st.number_input("Net Monthly Income (₹)", min_value=0, max_value=10000000, value=50000, step=1000)
        with c5: time_with_curr_empr = st.number_input("Time with Current Employer (months)", min_value=0, max_value=600, value=24)

        st.markdown('<div class="section-header">Trade Line History</div>', unsafe_allow_html=True)
        c6,c7,c8 = st.columns(3)
        with c6: age_oldest_tl  = st.number_input("Age of Oldest TL (months)", min_value=0, max_value=600, value=60)
        with c7: age_newest_tl  = st.number_input("Age of Newest TL (months)", min_value=0, max_value=600, value=12)
        with c8: tot_tl_closed_l12m = st.number_input("TL Closed in Last 12M", min_value=0, max_value=50, value=0)

        c9,c10,c11 = st.columns(3)
        with c9:  cc_tl        = st.number_input("Credit Card TLs",  min_value=0, max_value=20, value=1)
        with c10: home_tl      = st.number_input("Home Loan TLs",    min_value=0, max_value=10, value=0)
        with c11: pl_tl        = st.number_input("Personal Loan TLs",min_value=0, max_value=20, value=1)

        c12,c13,c14 = st.columns(3)
        with c12: secured_tl   = st.number_input("Secured TLs",   min_value=0, max_value=20, value=1)
        with c13: unsecured_tl = st.number_input("Unsecured TLs", min_value=0, max_value=20, value=2)
        with c14: other_tl     = st.number_input("Other TLs",     min_value=0, max_value=20, value=0)

        st.markdown('<div class="section-header">Payment & Delinquency History</div>', unsafe_allow_html=True)
        c15,c16,c17 = st.columns(3)
        with c15: time_since_recent_payment  = st.number_input("Time Since Recent Payment (mo)",  min_value=0, max_value=120, value=2)
        with c16: max_recent_level_of_deliq  = st.number_input("Max Recent Level of Delinquency", min_value=0, max_value=10,  value=0)
        with c17: recent_level_of_deliq      = st.number_input("Recent Level of Delinquency",     min_value=0, max_value=10,  value=0)

        c18,c19,c20 = st.columns(3)
        with c18: tot_missed_pmnt   = st.number_input("Total Missed Payments",        min_value=0, max_value=50, value=0)
        with c19: num_deliq_6_12mts = st.number_input("Delinquencies (6-12 months)",  min_value=0, max_value=20, value=0)
        with c20: num_times_60p_dpd = st.number_input("Times 60+ DPD",               min_value=0, max_value=20, value=0)

        c21,c22,c23 = st.columns(3)
        with c21: num_std_12mts = st.number_input("Standard Accounts Last 12M", min_value=0, max_value=20, value=2)
        with c22: num_sub       = st.number_input("Substandard Accounts",        min_value=0, max_value=20, value=0)
        with c23: num_sub_6mts  = st.number_input("Substandard Accounts (6M)",   min_value=0, max_value=20, value=0)

        c24,c25,c26 = st.columns(3)
        with c24: num_sub_12mts = st.number_input("Substandard Accounts (12M)", min_value=0, max_value=20, value=0)
        with c25: num_dbt       = st.number_input("Doubtful Accounts",           min_value=0, max_value=20, value=0)
        with c26: num_dbt_12mts = st.number_input("Doubtful Accounts (12M)",     min_value=0, max_value=20, value=0)

        num_lss = st.number_input("Loss Accounts", min_value=0, max_value=20, value=0)

        st.markdown('<div class="section-header">Credit Enquiry History</div>', unsafe_allow_html=True)
        c27,c28,c29 = st.columns(3)
        with c27: time_since_recent_enq = st.number_input("Time Since Recent Enquiry (mo)", min_value=0, max_value=120, value=3)
        with c28: enq_l3m               = st.number_input("Enquiries in Last 3 Months",     min_value=0, max_value=20,  value=1)
        with c29: cc_enq_l12m           = st.number_input("CC Enquiries Last 12M",           min_value=0, max_value=20,  value=0)
        pl_enq_l12m = st.number_input("PL Enquiries Last 12M", min_value=0, max_value=20, value=1)

        st.markdown('<div class="section-header">Percentage & Flag Features</div>', unsafe_allow_html=True)
        c30,c31 = st.columns(2)
        with c30:
            pct_tl_open_l6m       = st.slider("% TL Opened L6M",         0.0, 1.0, 0.20, 0.01)
            pct_tl_closed_l6m     = st.slider("% TL Closed L6M",         0.0, 1.0, 0.10, 0.01)
            pct_tl_closed_l12m    = st.slider("% TL Closed L12M",        0.0, 1.0, 0.15, 0.01)
            pct_pl_enq_l6m_of_ever= st.slider("% PL Enquiries L6M/Ever", 0.0, 1.0, 0.30, 0.01)
            pct_cc_enq_l6m_of_ever= st.slider("% CC Enquiries L6M/Ever", 0.0, 1.0, 0.20, 0.01)
        with c31:
            cc_flag = st.selectbox("CC Flag", [0,1], format_func=lambda x: "Yes" if x else "No")
            pl_flag = st.selectbox("PL Flag", [0,1], format_func=lambda x: "Yes" if x else "No")
            hl_flag = st.selectbox("HL Flag", [0,1], format_func=lambda x: "Yes" if x else "No")
            gl_flag = st.selectbox("GL Flag", [0,1], format_func=lambda x: "Yes" if x else "No")

        st.markdown('<div class="section-header">Product Enquiry Type</div>', unsafe_allow_html=True)
        c32,c33 = st.columns(2)
        with c32: last_prod_enq2  = st.selectbox("Last Product Enquiry",  ["ConsumerLoan","PL","AL","CC","HL","others"])
        with c33: first_prod_enq2 = st.selectbox("First Product Enquiry", ["ConsumerLoan","PL","AL","CC","HL","others"])

        st.markdown("<br>", unsafe_allow_html=True)
        submitted_expert = st.form_submit_button("🔍  Assess Credit Risk")

    if submitted_expert:
        edu_map = {'SSC':1,'12TH':2,'GRADUATE':3,'UNDER GRADUATE':3,
                   'PROFESSIONAL':3,'POST-GRADUATE':4,'OTHERS':1}

        base_features = {
            'pct_tl_open_L6M':pct_tl_open_l6m,'pct_tl_closed_L6M':pct_tl_closed_l6m,
            'Tot_TL_closed_L12M':tot_tl_closed_l12m,'pct_tl_closed_L12M':pct_tl_closed_l12m,
            'Tot_Missed_Pmnt':tot_missed_pmnt,'CC_TL':cc_tl,'Home_TL':home_tl,
            'PL_TL':pl_tl,'Secured_TL':secured_tl,'Unsecured_TL':unsecured_tl,
            'Other_TL':other_tl,'Age_Oldest_TL':age_oldest_tl,'Age_Newest_TL':age_newest_tl,
            'time_since_recent_payment':time_since_recent_payment,
            'max_recent_level_of_deliq':max_recent_level_of_deliq,
            'num_deliq_6_12mts':num_deliq_6_12mts,'num_times_60p_dpd':num_times_60p_dpd,
            'num_std_12mts':num_std_12mts,'num_sub':num_sub,'num_sub_6mts':num_sub_6mts,
            'num_sub_12mts':num_sub_12mts,'num_dbt':num_dbt,'num_dbt_12mts':num_dbt_12mts,
            'num_lss':num_lss,'recent_level_of_deliq':recent_level_of_deliq,
            'CC_enq_L12m':cc_enq_l12m,'PL_enq_L12m':pl_enq_l12m,
            'time_since_recent_enq':time_since_recent_enq,'enq_L3m':enq_l3m,
            'NETMONTHLYINCOME':net_monthly_income,'Time_With_Curr_Empr':time_with_curr_empr,
            'CC_Flag':cc_flag,'PL_Flag':pl_flag,
            'pct_PL_enq_L6m_of_ever':pct_pl_enq_l6m_of_ever,
            'pct_CC_enq_L6m_of_ever':pct_cc_enq_l6m_of_ever,
            'HL_Flag':hl_flag,'GL_Flag':gl_flag,
            'EDUCATION':edu_map[education],
            'MARITALSTATUS_Married':1 if marital_status=='Married' else 0,
            'MARITALSTATUS_Single': 1 if marital_status=='Single'  else 0,
            'GENDER_F':1 if gender=='F' else 0,'GENDER_M':1 if gender=='M' else 0,
            'last_prod_enq2_AL':          1 if last_prod_enq2=='AL'           else 0,
            'last_prod_enq2_CC':          1 if last_prod_enq2=='CC'           else 0,
            'last_prod_enq2_ConsumerLoan':1 if last_prod_enq2=='ConsumerLoan' else 0,
            'last_prod_enq2_HL':          1 if last_prod_enq2=='HL'           else 0,
            'last_prod_enq2_PL':          1 if last_prod_enq2=='PL'           else 0,
            'last_prod_enq2_others':      1 if last_prod_enq2=='others'       else 0,
            'first_prod_enq2_AL':          1 if first_prod_enq2=='AL'           else 0,
            'first_prod_enq2_CC':          1 if first_prod_enq2=='CC'           else 0,
            'first_prod_enq2_ConsumerLoan':1 if first_prod_enq2=='ConsumerLoan' else 0,
            'first_prod_enq2_HL':          1 if first_prod_enq2=='HL'           else 0,
            'first_prod_enq2_PL':          1 if first_prod_enq2=='PL'           else 0,
            'first_prod_enq2_others':      1 if first_prod_enq2=='others'       else 0,
        }

        key_metrics = [
            (age_oldest_tl,        "Oldest TL (mo)"),
            (enq_l3m,              "Enquiries L3M"),
            (max_recent_level_of_deliq, "Max Delinquency"),
            (f"₹{net_monthly_income:,}", "Monthly Income"),
            (num_std_12mts,        "Std Accounts 12M"),
        ]
        run_prediction(base_features, key_metrics)