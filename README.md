<div align="center">

# 🏦 Credit Risk Modelling

### End-to-end ML system predicting credit risk tiers (P1/P2/P3/P4) for loan applicants using XGBoost

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-3.2.0-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://credit-risk-modelling-app01.streamlit.app/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-7C3AED?style=for-the-badge)](https://shap.readthedocs.io)
[![Status](https://img.shields.io/badge/Status-Production-22C55E?style=for-the-badge)]()

<br/>

### 🚀 [**Try the Live Demo →**](https://credit-risk-modelling-app01.streamlit.app/)

<br/>

| 📦 Training Records | 🎯 CV Accuracy | 📊 CV Macro F1 | ⚡ P3 Recall |
|:---:|:---:|:---:|:---:|
| **42,064** | **78.09% ± 0.25%** | **0.6864 ± 0.38%** | **69.4% (tuned)** |

</div>

---

## 📌 Project Overview

This project builds a production-grade credit risk classification model trained on **42,064 customer records** from credit bureau data. The system predicts which risk tier a loan applicant falls into, enabling banks to make data-driven lending decisions with full model explainability via SHAP.

---

## 🎯 Risk Tier Classification

| Tier | Risk Level | Bank Action |
|:----:|:----------:|:-----------:|
| 🟢 **P1** | Very Low Risk | ✅ Approve — best rate |
| 🔵 **P2** | Low-Moderate Risk | ✅ Approve — standard rate |
| 🟡 **P3** | Moderate-High Risk | ⚠️ Conditional approval |
| 🔴 **P4** | High Risk | ❌ Reject |

---

## 🔧 Tech Stack

| Category | Tools |
|:---------|:------|
| **Language** | Python 3.13 |
| **ML Models** | XGBoost 3.2.0, Random Forest, Decision Tree |
| **Preprocessing** | Scikit-learn, Pandas, NumPy |
| **Imbalance Handling** | imbalanced-learn (SMOTE, SMOTEENN) |
| **Explainability** | SHAP |
| **Visualization** | Matplotlib |
| **Deployment** | Streamlit |

---

## ⚙️ Project Pipeline
```
01 → Data Loading & Cleaning       Sentinel value removal (−99999), null handling
02 → Feature Selection             Chi-square, VIF, ANOVA filtering
03 → Label Encoding                Ordinal + one-hot encoding
04 → Class Imbalance Handling      SMOTE, SMOTEENN, class weight tuning
05 → Model Training                Random Forest, XGBoost, Decision Tree
06 → Hyperparameter Tuning         Manual grid search optimization
07 → Model Explainability          SHAP value analysis
08 → Threshold Tuning              P3 recall optimized at threshold = 0.25
09 → Streamlit Deployment          Live interactive web app
```

---

## 📊 Model Performance

| Metric | Score |
|:-------|:-----:|
| CV Accuracy | **78.09%** ± 0.25% |
| CV Macro F1 | **0.6864** ± 0.38% |
| P3 Recall (tuned) | **69.4%** |

---

## 💡 Key Findings

- ✅ **XGBoost** outperformed Random Forest and Decision Tree across all metrics
- 📈 **Class weights** improved P3 F1 from `0.366` → `0.458`
- 🎯 **Threshold tuning** at P3 = 0.25 lifted recall to **69.4%**, reducing false negatives on risky applicants
- 🔍 **Top SHAP features:** `Age_Oldest_TL`, `enq_L3m`, `recent_level_of_deliq`

---

## 🚀 Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/ektashirsulla26-source/credit-risk-modelling.git
cd credit-risk-modelling

# 2. Install dependencies
pip install -r app/requirements.txt

# 3. Launch the app
cd app
streamlit run app_combined.py
```

---

## 👤 Author

**Ekta Shirsulla** — ML Engineer · Credit Risk · Financial ML

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ekta-shirsulla/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ektashirsulla26-source)

---

<div align="center">
<sub>Built with ❤️ using XGBoost · SHAP · Streamlit</sub>
</div>
