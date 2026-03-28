import pandas as pd
import numpy as np
import os

def generate_mental_health_data(n_samples=5000, filepath="data/mental_health_synthetic.csv"):
    """
    Generate synthetic, realistic mental health dataset.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.random.seed(42)
    
    age = np.random.randint(18, 65, n_samples)
    gender = np.random.choice(['Male', 'Female', 'Non-binary', 'Prefer not to say'], p=[0.45, 0.45, 0.08, 0.02], size=n_samples)
    
    # Simulate somewhat realistic correlations
    # More work hours -> less sleep, more stress
    work_study_hours = np.random.normal(8, 2.5, n_samples).clip(0, 16)
    
    # More screen time -> less sleep, more anxiety
    screen_time = np.random.normal(6, 3, n_samples).clip(0, 15)
    
    # Sleep depends on work and screen time
    sleep_hours = np.random.normal(8, 1.5, n_samples) - (work_study_hours * 0.1) - (screen_time * 0.1)
    sleep_hours = sleep_hours.clip(2, 12)
    
    physical_activity = np.random.normal(3, 2, n_samples).clip(0, 10)
    social_interaction = np.random.normal(5, 2.5, n_samples).clip(0, 10)
    
    # Stress depends on work, sleep (negative), physical activity (negative)
    stress_base = 3 + (work_study_hours * 0.3) + (screen_time * 0.2) - (sleep_hours * 0.4) - (physical_activity * 0.3)
    stress_level = (stress_base + np.random.normal(0, 1.5, n_samples)).clip(0, 10).astype(int)
    
    # Anxiety depends on stress, screen time
    anxiety_base = 2 + (stress_level * 0.5) + (screen_time * 0.2) - (social_interaction * 0.2)
    anxiety_level = (anxiety_base + np.random.normal(0, 1.5, n_samples)).clip(0, 10).astype(int)
    
    # Depression score depends on anxiety, social interaction (negative), physical activity (negative)
    depression_base = 1 + (anxiety_level * 0.4) + (stress_level * 0.3) - (social_interaction * 0.4) - (physical_activity * 0.2)
    depression_score = (depression_base + np.random.normal(0, 1.5, n_samples)).clip(0, 10).astype(int)
    
    # Introduce some missing values and outliers for data cleaning steps (as requested)
    mask_sleep = np.random.rand(n_samples) < 0.02
    sleep_hours[mask_sleep] = np.nan
    
    mask_activity = np.random.rand(n_samples) < 0.01
    physical_activity[mask_activity] = np.nan
    
    # Add a few outliers
    outlier_idx = np.random.choice(n_samples, 30, replace=False)
    screen_time[outlier_idx] = 22 # Unrealistically high screen time
    
    df = pd.DataFrame({
        'Age': age,
        'Gender': gender,
        'Sleep_Hours': sleep_hours,
        'Screen_Time': screen_time,
        'Work_Study_Hours': work_study_hours,
        'Physical_Activity': physical_activity,
        'Social_Interaction': social_interaction,
        'Stress_Level': stress_level,
        'Anxiety_Level': anxiety_level,
        'Depression_Score': depression_score
    })
    
    # Generate some duplicates to fulfill duplicate removal step
    duplicates = df.sample(85)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    df.to_csv(filepath, index=False)
    return df

def load_data(filepath="data/mental_health_synthetic.csv"):
    if not os.path.exists(filepath):
        return generate_mental_health_data(filepath=filepath)
    return pd.read_csv(filepath)

if __name__ == "__main__":
    generate_mental_health_data()
    print("Synthetic dataset generated successfully.")
