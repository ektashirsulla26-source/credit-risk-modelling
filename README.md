<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Credit Risk Modelling — README</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,300&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f8f9fc;
    --white: #ffffff;
    --surface: #f1f4f9;
    --border: #e2e8f0;
    --border2: #cbd5e1;
    --accent: #2563eb;
    --accent-light: #eff6ff;
    --accent2: #0891b2;
    --green: #16a34a;
    --green-light: #f0fdf4;
    --yellow: #ca8a04;
    --yellow-light: #fefce8;
    --red: #dc2626;
    --red-light: #fef2f2;
    --purple: #7c3aed;
    --purple-light: #f5f3ff;
    --orange: #ea580c;
    --text: #0f172a;
    --text-muted: #64748b;
    --text-dim: #475569;
    --mono: 'Space Mono', monospace;
    --sans: 'DM Sans', sans-serif;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    line-height: 1.7;
    min-height: 100vh;
  }

  .container {
    max-width: 880px;
    margin: 0 auto;
    padding: 40px 24px 80px;
  }

  /* HERO */
  .hero {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 52px 48px 44px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
  }

  .hero::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 380px; height: 380px;
    background: radial-gradient(circle at top right, #eff6ff 0%, transparent 65%);
    pointer-events: none;
  }

  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-bottom: 22px;
  }

  .badge {
    font-family: var(--mono);
    font-size: 10.5px;
    padding: 4px 10px;
    border-radius: 5px;
    border: 1px solid;
    letter-spacing: 0.04em;
  }

  .badge-blue  { color: #1d4ed8; border-color: #bfdbfe; background: #eff6ff; }
  .badge-green { color: #15803d; border-color: #bbf7d0; background: #f0fdf4; }
  .badge-purple{ color: #6d28d9; border-color: #ddd6fe; background: #f5f3ff; }
  .badge-cyan  { color: #0e7490; border-color: #a5f3fc; background: #ecfeff; }
  .badge-slate { color: #475569; border-color: #e2e8f0; background: #f8fafc; }

  .hero-title {
    font-family: var(--mono);
    font-size: clamp(28px, 4vw, 40px);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 14px;
    color: var(--text);
    letter-spacing: -0.03em;
  }

  .hero-title span { color: var(--accent); }

  .hero-desc {
    font-size: 15.5px;
    color: var(--text-dim);
    font-weight: 300;
    max-width: 580px;
    margin-bottom: 32px;
  }

  .demo-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: var(--accent);
    color: #fff;
    text-decoration: none;
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
    padding: 11px 22px;
    border-radius: 8px;
    letter-spacing: 0.06em;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25);
  }

  .demo-btn:hover {
    background: #1d4ed8;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(37,99,235,0.3);
  }

  .live-dot {
    width: 7px; height: 7px;
    background: #93c5fd;
    border-radius: 50%;
    animation: pulse 1.6s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.75); }
  }

  /* STATS BAR */
  .stats-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }

  .stat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
  }

  .stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 14px 14px;
  }

  .stat-card:nth-child(1)::after { background: var(--accent); }
  .stat-card:nth-child(2)::after { background: var(--green); }
  .stat-card:nth-child(3)::after { background: #d97706; }

  .stat-value {
    font-family: var(--mono);
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 3px;
    letter-spacing: -0.02em;
  }

  .stat-card:nth-child(1) .stat-value { color: var(--accent); }
  .stat-card:nth-child(2) .stat-value { color: var(--green); }
  .stat-card:nth-child(3) .stat-value { color: #d97706; }

  .stat-label {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 500;
  }

  /* SECTION */
  .section { margin-bottom: 24px; }

  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
  }

  .section-icon {
    width: 30px; height: 30px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
  }

  .icon-blue   { background: #eff6ff; border: 1px solid #bfdbfe; }
  .icon-green  { background: #f0fdf4; border: 1px solid #bbf7d0; }
  .icon-purple { background: #f5f3ff; border: 1px solid #ddd6fe; }
  .icon-cyan   { background: #ecfeff; border: 1px solid #a5f3fc; }
  .icon-orange { background: #fff7ed; border: 1px solid #fed7aa; }
  .icon-yellow { background: #fefce8; border: 1px solid #fde68a; }
  .icon-slate  { background: #f8fafc; border: 1px solid #e2e8f0; }

  .section-title {
    font-family: var(--mono);
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-muted);
  }

  .card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  /* RISK TIERS */
  .tier-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }

  .tier-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, border-color 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .tier-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border-color: var(--border2);
  }

  .tier-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 14px 14px 0 0;
  }

  .tier-p1::before { background: var(--green); }
  .tier-p2::before { background: var(--accent); }
  .tier-p3::before { background: #d97706; }
  .tier-p4::before { background: var(--red); }

  .tier-label {
    font-family: var(--mono);
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 2px;
  }

  .tier-p1 .tier-label { color: var(--green); }
  .tier-p2 .tier-label { color: var(--accent); }
  .tier-p3 .tier-label { color: #d97706; }
  .tier-p4 .tier-label { color: var(--red); }

  .tier-risk {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
    color: var(--text-muted);
  }

  .tier-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12.5px;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 500;
  }

  .tier-p1 .tier-chip { background: var(--green-light); color: var(--green); }
  .tier-p2 .tier-chip { background: var(--accent-light); color: var(--accent); }
  .tier-p3 .tier-chip { background: var(--yellow-light); color: #92400e; }
  .tier-p4 .tier-chip { background: var(--red-light); color: var(--red); }

  /* PIPELINE */
  .pipeline { padding: 24px 28px; }

  .pipeline-step {
    display: flex;
    align-items: flex-start;
  }

  .step-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    width: 36px;
  }

  .step-dot {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: #eff6ff;
    border: 2px solid #bfdbfe;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono);
    font-size: 10px;
    color: var(--accent);
    font-weight: 700;
    flex-shrink: 0;
  }

  .step-line {
    width: 2px;
    height: 28px;
    background: var(--border);
  }

  .step-body {
    flex: 1;
    padding: 4px 0 24px 16px;
  }

  .step-name {
    font-family: var(--mono);
    font-size: 12.5px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 2px;
  }

  .step-desc {
    font-size: 13px;
    color: var(--text-muted);
  }

  /* PERFORMANCE */
  .perf-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }

  .perf-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .perf-value {
    font-family: var(--mono);
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .perf-label {
    font-size: 11.5px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 600;
    margin-bottom: 6px;
  }

  .perf-sub {
    font-family: var(--mono);
    font-size: 10.5px;
    color: var(--text-muted);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
  }

  /* TECH STACK */
  .tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(128px, 1fr));
    gap: 10px;
  }

  .tech-chip {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .tech-chip:hover {
    border-color: #bfdbfe;
    box-shadow: 0 2px 8px rgba(37,99,235,0.08);
    color: var(--text);
  }

  .tech-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  /* FINDINGS */
  .findings-list { display: flex; flex-direction: column; gap: 10px; }

  .finding-item {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 13px 16px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
    font-size: 13.5px;
    color: var(--text-dim);
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    transition: border-color 0.2s;
  }

  .finding-item:hover { border-color: #bfdbfe; }

  .finding-arrow {
    color: var(--accent);
    font-weight: 700;
    flex-shrink: 0;
    margin-top: 2px;
    font-size: 14px;
  }

  code {
    font-family: var(--mono);
    font-size: 11.5px;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 1px 6px;
    border-radius: 4px;
    color: var(--accent2);
  }

  /* CODE BLOCK */
  .code-block {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
    background: var(--white);
  }

  .code-dots { display: flex; gap: 6px; }
  .code-dots span { width: 10px; height: 10px; border-radius: 50%; }
  .code-dots .d1 { background: #fca5a5; }
  .code-dots .d2 { background: #fcd34d; }
  .code-dots .d3 { background: #86efac; }

  .code-lang {
    font-family: var(--mono);
    font-size: 10.5px;
    color: var(--text-muted);
    letter-spacing: 0.1em;
  }

  pre {
    padding: 20px 24px;
    font-family: var(--mono);
    font-size: 12.5px;
    line-height: 1.75;
    overflow-x: auto;
    color: #334155;
  }

  .cm { color: #94a3b8; }
  .ck { color: #2563eb; }
  .cs { color: #16a34a; }
  .co { color: #ea580c; }

  /* AUTHOR */
  .author-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  }

  .author-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #bfdbfe, #ddd6fe);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono);
    font-size: 15px;
    font-weight: 700;
    color: var(--accent);
    flex-shrink: 0;
  }

  .author-left {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .author-info h3 {
    font-family: var(--mono);
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 3px;
  }

  .author-info p {
    font-size: 12.5px;
    color: var(--text-muted);
  }

  .author-links { display: flex; gap: 10px; }

  .author-link {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: var(--mono);
    font-size: 11.5px;
    padding: 8px 14px;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.2s;
    font-weight: 700;
    letter-spacing: 0.04em;
  }

  .link-linkedin {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: var(--accent);
  }

  .link-github {
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-dim);
  }

  .author-link:hover { opacity: 0.8; transform: translateY(-1px); }

  @media (max-width: 600px) {
    .hero { padding: 32px 22px 28px; }
    .tier-grid, .stats-bar, .perf-grid { grid-template-columns: 1fr; }
    .author-card { flex-direction: column; }
    .author-left { flex-direction: column; text-align: center; }
  }
</style>
</head>
<body>
<div class="container">

  <!-- HERO -->
  <div class="hero">
    <div class="badge-row">
      <span class="badge badge-blue">Python 3.13</span>
      <span class="badge badge-green">XGBoost 3.2.0</span>
      <span class="badge badge-purple">SHAP</span>
      <span class="badge badge-cyan">Streamlit</span>
      <span class="badge badge-slate">End-to-End ML</span>
    </div>
    <h1 class="hero-title">Credit Risk<br><span>Modelling</span></h1>
    <p class="hero-desc">
      An end-to-end machine learning system that classifies loan applicants into
      risk tiers (P1–P4) using XGBoost — from raw bureau data to live web deployment.
    </p>
    <a class="demo-btn" href="https://credit-risk-modelling-app01.streamlit.app/" target="_blank">
      <span class="live-dot"></span>
      LIVE DEMO
    </a>
  </div>

  <!-- STATS -->
  <div class="stats-bar">
    <div class="stat-card">
      <div class="stat-value">42,064</div>
      <div class="stat-label">Training Records</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">78.09%</div>
      <div class="stat-label">CV Accuracy</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">69.4%</div>
      <div class="stat-label">P3 Recall (Tuned)</div>
    </div>
  </div>

  <!-- RISK TIERS -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-blue">⚡</div>
      <span class="section-title">Risk Tier Classification</span>
    </div>
    <div class="tier-grid">
      <div class="tier-card tier-p1">
        <div class="tier-label">P1</div>
        <div class="tier-risk">Very Low Risk</div>
        <div class="tier-chip">✓ Approve — best rate</div>
      </div>
      <div class="tier-card tier-p2">
        <div class="tier-label">P2</div>
        <div class="tier-risk">Low-Moderate Risk</div>
        <div class="tier-chip">✓ Approve — standard rate</div>
      </div>
      <div class="tier-card tier-p3">
        <div class="tier-label">P3</div>
        <div class="tier-risk">Moderate-High Risk</div>
        <div class="tier-chip">⚠ Conditional approval</div>
      </div>
      <div class="tier-card tier-p4">
        <div class="tier-label">P4</div>
        <div class="tier-risk">High Risk</div>
        <div class="tier-chip">✕ Reject</div>
      </div>
    </div>
  </div>

  <!-- PIPELINE -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-purple">⚙</div>
      <span class="section-title">Project Pipeline</span>
    </div>
    <div class="card">
      <div class="pipeline">
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">01</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Data Loading & Cleaning</div><div class="step-desc">Sentinel value removal (−99999), null handling across 42K records</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">02</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Feature Selection</div><div class="step-desc">Chi-square, VIF, and ANOVA-based filtering for signal quality</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">03</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Label Encoding</div><div class="step-desc">Ordinal encoding + one-hot encoding for categorical features</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">04</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Class Imbalance Handling</div><div class="step-desc">SMOTE, SMOTEENN oversampling + class weight adjustments</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">05</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Model Training</div><div class="step-desc">Benchmarked Random Forest, XGBoost, and Decision Tree</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">06</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Hyperparameter Tuning</div><div class="step-desc">Manual grid search for XGBoost optimization</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">07</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Model Explainability</div><div class="step-desc">SHAP value analysis for feature importance and interpretability</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">08</div><div class="step-line"></div></div>
          <div class="step-body"><div class="step-name">Threshold Tuning</div><div class="step-desc">P3 recall optimized by setting decision threshold to 0.25</div></div>
        </div>
        <div class="pipeline-step">
          <div class="step-col"><div class="step-dot">09</div></div>
          <div class="step-body" style="padding-bottom: 0;"><div class="step-name">Streamlit Deployment</div><div class="step-desc">Live interactive web app for real-time applicant scoring</div></div>
        </div>
      </div>
    </div>
  </div>

  <!-- PERFORMANCE -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-green">📊</div>
      <span class="section-title">Model Performance</span>
    </div>
    <div class="perf-grid">
      <div class="perf-card">
        <div class="perf-value" style="color: var(--accent);">78.09%</div>
        <div class="perf-label">CV Accuracy</div>
        <div class="perf-sub">± 0.25%</div>
      </div>
      <div class="perf-card">
        <div class="perf-value" style="color: var(--accent2);">0.6864</div>
        <div class="perf-label">CV Macro F1</div>
        <div class="perf-sub">± 0.38%</div>
      </div>
      <div class="perf-card">
        <div class="perf-value" style="color: #d97706;">69.4%</div>
        <div class="perf-label">P3 Recall (Tuned)</div>
        <div class="perf-sub">threshold 0.25</div>
      </div>
    </div>
  </div>

  <!-- TECH STACK -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-cyan">🔧</div>
      <span class="section-title">Tech Stack</span>
    </div>
    <div class="tech-grid">
      <div class="tech-chip"><span class="tech-dot" style="background:#16a34a;"></span>Python 3.13</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#ea580c;"></span>XGBoost 3.2.0</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#2563eb;"></span>Scikit-learn</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#7c3aed;"></span>imbalanced-learn</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#0891b2;"></span>SHAP</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#db2777;"></span>Streamlit</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#ca8a04;"></span>Pandas</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#0d9488;"></span>NumPy</div>
      <div class="tech-chip"><span class="tech-dot" style="background:#d97706;"></span>Matplotlib</div>
    </div>
  </div>

  <!-- KEY FINDINGS -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-yellow">💡</div>
      <span class="section-title">Key Findings</span>
    </div>
    <div class="findings-list">
      <div class="finding-item">
        <span class="finding-arrow">→</span>
        XGBoost outperformed both Random Forest and Decision Tree across all evaluation metrics
      </div>
      <div class="finding-item">
        <span class="finding-arrow">→</span>
        Class weights improved P3 F1 score from <strong style="color:var(--text);">0.366</strong> → <strong style="color:var(--green);">0.458</strong>, a significant uplift for the high-risk class
      </div>
      <div class="finding-item">
        <span class="finding-arrow">→</span>
        Threshold tuning at P3 = 0.25 lifted recall to <strong style="color:#d97706;">69.4%</strong>, reducing dangerous false negatives on risky applicants
      </div>
      <div class="finding-item">
        <span class="finding-arrow">→</span>
        Top SHAP features: <code>Age_Oldest_TL</code>, <code>enq_L3m</code>, <code>recent_level_of_deliq</code>
      </div>
    </div>
  </div>

  <!-- INSTALLATION -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-orange">▶</div>
      <span class="section-title">Run Locally</span>
    </div>
    <div class="code-block">
      <div class="code-header">
        <div class="code-dots">
          <span class="d1"></span><span class="d2"></span><span class="d3"></span>
        </div>
        <span class="code-lang">BASH</span>
      </div>
      <pre><span class="cm"># 1. Clone the repository</span>
<span class="ck">git</span> <span class="cs">clone</span> https://github.com/ektashirsulla26-source/credit-risk-modelling.git
<span class="ck">cd</span> credit-risk-modelling

<span class="cm"># 2. Install dependencies</span>
<span class="ck">pip</span> <span class="cs">install</span> <span class="co">-r</span> app/requirements.txt

<span class="cm"># 3. Launch the Streamlit app</span>
<span class="ck">cd</span> app
<span class="ck">streamlit</span> <span class="cs">run</span> app_combined.py</pre>
    </div>
  </div>

  <!-- AUTHOR -->
  <div class="section">
    <div class="section-header">
      <div class="section-icon icon-slate">👤</div>
      <span class="section-title">Author</span>
    </div>
    <div class="author-card">
      <div class="author-left">
        <div class="author-avatar">ES</div>
        <div class="author-info">
          <h3>Ekta Shirsulla</h3>
          <p>ML Engineer · Credit Risk · Financial ML</p>
        </div>
      </div>
      <div class="author-links">
        <a class="author-link link-linkedin" href="https://www.linkedin.com/in/ekta-shirsulla/" target="_blank">in&nbsp; LinkedIn</a>
        <a class="author-link link-github" href="https://github.com/ektashirsulla26-source" target="_blank">⌥&nbsp; GitHub</a>
      </div>
    </div>
  </div>

</div>
</body>
</html>
