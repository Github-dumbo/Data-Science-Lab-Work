# MindScope™ – Mental Health Analytics Dashboard

## Description
MindScope™ is an interactive, production-grade analytics dashboard that analyzes mental health data and provides deep insights into the relationship between lifestyle factors (sleep, screen time, physical activity) and mental health outcomes (stress, anxiety, depression). It features a sleek, intuitive UI, advanced visualizations, and an integrated machine learning system for stress risk prediction.

## Dataset
* Source: Generative Synthetic Script
* Description of data: Highly realistic generated dataset detailing attributes such as Age, Gender, Sleep Hours, Screen Time, Work/Study Hours, Physical Activity, Social Interaction, Stress Level, Anxiety Level, and Depression Score.

## Steps Performed
1. Data Cleaning: Duplicate removal, missing value handling via median imputation, and outlier capping for realistic distributions.
2. Exploratory Data Analysis: Deep insights extraction regarding top drivers of stress and common behavioral patterns.
3. Visualization: High-quality Matplotlib & Seaborn plots tailored with a dark SaaS-inspired theme, displaying correlation heatmaps, feature distributions, and scatter plots.
4. Model Building: Data preprocessing (Label Encoding, Standard Scaling) and training of Logistic Regression, Decision Tree, and Random Forest models with auto-selection of the best-performing model.

## Results
* Key findings: Sleep duration and physical activity show a strong negative correlation with stress, while prolonged screen time significantly drives anxiety levels.
* Metrics: The Random Forest classifier routinely achieves strong accuracy (>85%) in identifying High Stress Risk users based on behavioral profiles, consistently outperforming the base logistic regression and decision trees.

## Tools Used
* Python
* NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Streamlit

## How to Run
1. Clone the repository
2. Install dependencies using:
   `pip install -r requirements.txt`
3. Run the app:
   `streamlit run app.py`
4. Open the local URL in your browser

## Conclusion
MindScope demonstrates how modern data science techniques can uncover critical insights into the modern lifestyle context. By identifying key stressors and utilizing robust predictive modeling, organizations and individuals can make data-backed decisions toward improving overall mental well-being.

## Author
Nehal Santosh Lashkar
