import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def clean_data(df):
    """
    Cleans the given dataframe based on defined rules.
    Returns the cleaned dataframe and a summary of actions taken.
    """
    cleaning_summary = {}
    
    # 1. Duplicate removal
    initial_shape = df.shape
    df = df.drop_duplicates()
    cleaning_summary['duplicates_removed'] = initial_shape[0] - df.shape[0]
    
    # 2. Missing value handling
    # We'll use median imputation for numerical values as it's robust to outliers
    missing_before = df.isnull().sum().sum()
    if 'Sleep_Hours' in df.columns:
        df['Sleep_Hours'].fillna(df['Sleep_Hours'].median(), inplace=True)
    if 'Physical_Activity' in df.columns:
        df['Physical_Activity'].fillna(df['Physical_Activity'].median(), inplace=True)
    cleaning_summary['missing_values_filled'] = missing_before
    
    # 3. Outlier handling
    # Cap screen time at a logical maximum (e.g., 24 hours but let's say 18 is upper realistic limit)
    outliers_before = (df['Screen_Time'] > 18).sum()
    df.loc[df['Screen_Time'] > 18, 'Screen_Time'] = 18
    cleaning_summary['outliers_capped'] = outliers_before
    
    return df, cleaning_summary

def preprocess_for_ml(df):
    """
    Prepares data for machine learning models.
    Returns X (features), y (target), label_encoders, and scaler.
    """
    df_encoded = df.copy()
    
    # Target Variable Formulation
    # We will predict "High Risk" based on a composite metric, but for simplicity,
    # let's predict if Stress_Level > 6 (0 = Low/Mod, 1 = High)
    df_encoded['High_Stress_Risk'] = (df_encoded['Stress_Level'] > 6).astype(int)
    
    # Features we use for prediction (we drop the answers that would perfectly correlate backwards)
    features = ['Age', 'Gender', 'Sleep_Hours', 'Screen_Time', 'Work_Study_Hours', 'Physical_Activity', 'Social_Interaction']
    X = df_encoded[features]
    y = df_encoded['High_Stress_Risk']
    
    # 4. Encoding categorical data
    label_encoders = {}
    if 'Gender' in X.columns:
        le = LabelEncoder()
        # Convert to numpy array safely before assignment to prevent SettingWithCopyWarning
        v = le.fit_transform(X['Gender'])
        X = X.copy()
        X['Gender'] = v
        label_encoders['Gender'] = le
        
    # 5. Feature scaling
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    
    return X_scaled, y, label_encoders, scaler

def get_eda_summary(df):
    """
    Generates summary statistics for EDA.
    """
    return df.describe()

def get_correlation_matrix(df):
    """
    Returns the correlation matrix for numerical features.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr()
