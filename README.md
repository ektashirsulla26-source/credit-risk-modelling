# Credit Risk Modelling

An end-to-end machine learning project that predicts credit risk tiers 
(P1/P2/P3/P4) for loan applicants using XGBoost with full deployment.

## Live Demo
[Click here to try the app](https://ektashirsulla26-source/credit-risk-modelling.streamlit.app)

## Project Overview
This project builds a credit risk classification model trained on 42,064 
customer records from credit bureau data.

### Risk Tiers
| Tier | Risk Level | Bank Action |
|------|-----------|-------------|
| P1 | Very Low Risk | Approve — best rate |
| P2 | Low-Moderate Risk | Approve — standard rate |
| P3 | Moderate-High Risk | Conditional approval |
| P4 | High Risk | Reject |

## Tech Stack
- Python 3.13
- XGBoost 3.2.0
- Scikit-learn
- Imbalanced-learn (SMOTE, SMOTEENN)
- SHAP for explainability
- Streamlit for deployment
- Pandas, NumPy, Matplotlib

## Project Pipeline
1. Data Loading and Cleaning (sentinel value -99999 removal)
2. Feature Selection (Chi-square, VIF, ANOVA)
3. Label Encoding (ordinal + one-hot)
4. Class Imbalance Handling (SMOTE, SMOTEENN, Class Weights)
5. Model Training (Random Forest, XGBoost, Decision Tree)
6. Hyperparameter Tuning (Manual Grid Search)
7. Model Explainability (SHAP values)
8. Threshold Tuning (P3 recall optimization)
9. Streamlit Web App Deployment

## Model Performance
| Metric | Score |
|--------|-------|
| CV Accuracy | 78.09% ± 0.25% |
| CV Macro F1 | 0.6864 ± 0.38% |
| P3 Recall (tuned) | 69.4% |

## Key Findings
- XGBoost outperformed Random Forest and Decision Tree
- Class weights improved P3 F1 from 0.366 to 0.458
- Threshold tuning (P3 = 0.25) improved P3 Recall to 69.4%
- Top features: Age_Oldest_TL, enq_L3m, recent_level_of_deliq

## How to Run Locally
```bash
# Clone the repository
git clone https://github.com/ektashirsulla26-source/credit-risk-modelling.git
cd credit-risk-modelling

# Install dependencies
pip install -r app/requirements.txt

# Run the app
cd app
streamlit run app_combined.py
```

## Author
Your Name — [LinkedIn](https://www.linkedin.com/in/ekta-shirsulla/) | 
[GitHub](https://github.com/ektashirsulla26-source)
