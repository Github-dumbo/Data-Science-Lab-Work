import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

def train_models(X, y):
    """
    Trains Logistic Regression, Decision Tree, and Random Forest models.
    Returns the models, their accuracies, and confusion matrices.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100)
    }
    
    results = {}
    best_model_name = None
    best_accuracy = 0
    best_model = None
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': acc,
            'confusion_matrix': cm
        }
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model = model
            
    return results, best_model_name, best_model, X_train.columns

def predict_stress(model, input_data, scaler, features_order):
    """
    Predicts using the selected model.
    """
    # Create DataFrame to maintain feature names for scaler
    df_input = pd.DataFrame([input_data], columns=features_order)
    input_scaled = scaler.transform(df_input)
    prediction = model.predict(input_scaled)
    # prediction returns 1 (High Risk) or 0 (Low Risk)
    return prediction[0]
