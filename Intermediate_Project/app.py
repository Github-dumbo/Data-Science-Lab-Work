import streamlit as st
import pandas as pd
import numpy as np

# Set page config first
st.set_page_config(page_title="MindScope™ Analytics", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Startup/SaaS look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0F111A;
        color: #E2E8F0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E202B;
        border-right: 1px solid #333A4D;
    }
    
    /* Metrics blocks */
    [data-testid="stMetricValue"] {
        color: #3b82f6;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

from data_gen import load_data
from data_processing import clean_data, preprocess_for_ml, get_eda_summary
from visualizations import (get_correlation_heatmap, get_stress_vs_sleep, 
                            get_screen_time_vs_anxiety, get_distributions, 
                            get_behavior_boxplots, get_confusion_matrix_plot)
from ml_models import train_models, predict_stress

# Initialize Session State
if 'data' not in st.session_state:
    with st.spinner("Loading Data & Training Models..."):
        raw_df = load_data()
        cleaned_df, cleaning_summary = clean_data(raw_df)
        X, y, encoders, scaler = preprocess_for_ml(cleaned_df)
        results, best_model_name, best_model, features_order = train_models(X, y)
        
        st.session_state['raw_df'] = raw_df
        st.session_state['cleaned_df'] = cleaned_df
        st.session_state['cleaning_summary'] = cleaning_summary
        st.session_state['X'] = X
        st.session_state['y'] = y
        st.session_state['encoders'] = encoders
        st.session_state['scaler'] = scaler
        st.session_state['results'] = results
        st.session_state['best_model_name'] = best_model_name
        st.session_state['best_model'] = best_model
        st.session_state['features_order'] = features_order

def main():
    st.sidebar.title("🧠 MindScope™")
    st.sidebar.caption("“Understand your mind. Backed by data.”")
    st.sidebar.markdown("---")
    
    pages = ["Overview", "Data Insights", "Visual Analytics", "Model Comparison", "Prediction Tool"]
    choice = st.sidebar.radio("Navigation", pages)
    
    df = st.session_state['cleaned_df']
    
    if choice == "Overview":
        st.title("Welcome to MindScope™")
        st.markdown("MindScope is a production-grade analytics dashboard designed to uncover the relationships between lifestyle factors and mental health outcomes.")
        
        st.header("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", len(df))
        col2.metric("Avg Stress Level", f"{df['Stress_Level'].mean():.2f}/10")
        col3.metric("Avg Sleep Hours", f"{df['Sleep_Hours'].mean():.1f} hr")
        col4.metric("High Risk Users", f"{(df['Stress_Level'] > 6).sum()}")
        
        st.markdown("---")
        st.header("Data Collection & Cleaning")
        col_clean, col_raw = st.columns(2)
        with col_clean:
            st.subheader("Cleaning Summary")
            summary = st.session_state['cleaning_summary']
            st.info(f"🗑️ Duplicates Removed: {summary['duplicates_removed']}")
            st.info(f"🔄 Missing Values Handled: {summary['missing_values_filled']}")
            st.info(f"⚠️ Outliers Capped: {summary['outliers_capped']}")
        with col_raw:
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
    elif choice == "Data Insights":
        st.title("Data Insights & Statistics")
        st.markdown("Explore summary statistics and top drivers of mental health indicators.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Top 3 Drivers of Stress")
            st.success("1. **Low Sleep Hours** (Strong Negative Correlation)")
            st.success("2. **High Work/Study Hours** (Positive Correlation)")
            st.success("3. **Low Physical Activity** (Negative Correlation)")
            
        with col2:
            st.markdown("### Behavioral Patterns")
            st.warning("• Users with prolonged screen time report significantly higher anxiety.")
            st.warning("• Social interaction acts as a buffer against depression and isolation.")
            st.warning("• Optimal sleep strongly mitigates work-related stress levels.")
            
        st.markdown("---")
        st.subheader("Summary Statistics")
        st.dataframe(get_eda_summary(df), use_container_width=True)

    elif choice == "Visual Analytics":
        st.title("Visual Analytics")
        st.markdown("Deep dive into the data using advanced visual representations.")
        
        st.subheader("Feature Distributions")
        st.pyplot(get_distributions(df))
        
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(get_stress_vs_sleep(df))
            st.pyplot(get_behavior_boxplots(df))
        with col2:
            st.pyplot(get_correlation_heatmap(df))
            st.pyplot(get_screen_time_vs_anxiety(df))

    elif choice == "Model Comparison":
        st.title("Machine Learning Models")
        st.markdown("We trained multiple models to predict High Stress Risk (Stress Level > 6).")
        
        results = st.session_state['results']
        best_name = st.session_state['best_model_name']
        
        st.success(f"🏆 Best Model: **{best_name}** with **{results[best_name]['accuracy']*100:.2f}%** Accuracy")
        
        cols = st.columns(3)
        for idx, (name, metrics) in enumerate(results.items()):
            with cols[idx]:
                st.markdown(f"### {name}")
                st.metric("Accuracy", f"{metrics['accuracy']*100:.2f}%")
                st.pyplot(get_confusion_matrix_plot(metrics['confusion_matrix'], f"{name} Matrix"))

    elif choice == "Prediction Tool":
        st.title("Prediction Tool")
        st.markdown("Predict mental health risk based on lifestyle factors using our best ML model.")
        
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=18, max_value=100, value=25)
                gender = st.selectbox("Gender", ['Male', 'Female', 'Non-binary', 'Prefer not to say'])
                sleep = st.slider("Sleep Hours", 0.0, 24.0, 7.0)
                screen = st.slider("Screen Time (Hours)", 0.0, 24.0, 6.0)
                
            with col2:
                work = st.slider("Work/Study Hours", 0.0, 24.0, 8.0)
                activity = st.slider("Physical Activity (0-10)", 0.0, 10.0, 5.0)
                social = st.slider("Social Interaction (0-10)", 0.0, 10.0, 7.0)
                
            submit = st.form_submit_button("Predict Risk")
            
        if submit:
            # Prepare input
            encoders = st.session_state['encoders']
            gender_encoded = encoders['Gender'].transform([gender])[0] if 'Gender' in encoders else 0
            
            # Map input to exact feature order
            input_dict = {
                'Age': age,
                'Gender': gender_encoded,
                'Sleep_Hours': sleep,
                'Screen_Time': screen,
                'Work_Study_Hours': work,
                'Physical_Activity': activity,
                'Social_Interaction': social
            }
            
            prediction = predict_stress(
                st.session_state['best_model'], 
                input_dict, 
                st.session_state['scaler'], 
                st.session_state['features_order']
            )
            
            st.markdown("---")
            if prediction == 1:
                st.error("🚨 **Prediction: High Stress Risk**")
                st.markdown("We recommend reducing screen time, optimizing sleep, and increasing physical activity.")
            else:
                st.success("✅ **Prediction: Low/Moderate Stress Risk**")
                st.markdown("Great job maintaining a balanced lifestyle!")

if __name__ == '__main__':
    main()
