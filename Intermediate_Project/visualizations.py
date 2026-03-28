import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib

# Use Agg backend for thread safety in Streamlit
matplotlib.use('Agg')

def set_style():
    """Applies a professional dark calm theme to charts."""
    sns.set_theme(style="darkgrid", rc={
        "axes.facecolor": "#1E202B",      # Dark blueish gray background
        "figure.facecolor": "#1E202B",
        "axes.edgecolor": "#333A4D",
        "grid.color": "#333A4D",
        "text.color": "#E2E8F0",
        "axes.labelcolor": "#E2E8F0",
        "xtick.color": "#cbd5e1",
        "ytick.color": "#cbd5e1",
        "lines.color": "#3b82f6"
    })
    
def get_correlation_heatmap(df):
    set_style()
    fig, ax = plt.subplots(figsize=(10, 8))
    # Select only numerical
    corr = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", ax=ax, cbar=True, center=0, 
                linewidths=0.5, linecolor="#1E202B")
    ax.set_title("Correlation Heatmap of Mental Health Factors", fontsize=14, color='white', pad=20)
    fig.tight_layout()
    return fig

def get_stress_vs_sleep(df):
    set_style()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # We create a High_Stress column if it doesn't exist for coloring
    df_plot = df.copy()
    if 'High_Stress' not in df_plot.columns:
        df_plot['High_Stress'] = (df_plot['Stress_Level'] > 6).astype(int).map({0: 'Low/Moderate', 1: 'High Stress'})
        
    sns.scatterplot(data=df_plot, x='Sleep_Hours', y='Stress_Level', hue='High_Stress', 
                    palette={'Low/Moderate': '#3b82f6', 'High Stress': '#ef4444'}, alpha=0.6, ax=ax)
    ax.set_title("Stress Level vs Sleep Hours", fontsize=14, color='white', pad=15)
    ax.set_xlabel("Sleep Hours")
    ax.set_ylabel("Stress Level")
    fig.tight_layout()
    return fig

def get_screen_time_vs_anxiety(df):
    set_style()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(data=df, x='Screen_Time', y='Anxiety_Level', scatter_kws={'alpha':0.3, 'color':'#8b5cf6'}, line_kws={'color':'#ef4444'}, ax=ax)
    ax.set_title("Screen Time vs Anxiety Level", fontsize=14, color='white', pad=15)
    ax.set_xlabel("Screen Time (Hours)")
    ax.set_ylabel("Anxiety Level")
    fig.tight_layout()
    return fig

def get_distributions(df):
    set_style()
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.histplot(df['Stress_Level'], bins=10, kde=True, color='#f43f5e', ax=axes[0])
    axes[0].set_title("Distribution of Stress Levels", color='white')
    axes[0].set_xlabel("Stress Level")
    
    sns.histplot(df['Sleep_Hours'], bins=15, kde=True, color='#0ea5e9', ax=axes[1])
    axes[1].set_title("Distribution of Sleep Hours", color='white')
    axes[1].set_xlabel("Sleep Hours")
    
    sns.histplot(df['Screen_Time'], bins=15, kde=True, color='#8b5cf6', ax=axes[2])
    axes[2].set_title("Distribution of Screen Time", color='white')
    axes[2].set_xlabel("Screen Time")
    
    fig.tight_layout()
    return fig

def get_behavior_boxplots(df):
    set_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    # Categorize physical activity to show impact on stress
    df_plot = df.copy()
    df_plot['Activity_Level'] = pd.cut(df_plot['Physical_Activity'], bins=[-1, 3, 6, 11], labels=['Low', 'Moderate', 'High'])
    
    sns.boxplot(data=df_plot, x='Activity_Level', y='Stress_Level', palette=['#f43f5e', '#f59e0b', '#10b981'], ax=ax)
    ax.set_title("Stress Level by Physical Activity", fontsize=14, color='white', pad=15)
    ax.set_xlabel("Physical Activity Level")
    ax.set_ylabel("Stress Level")
    fig.tight_layout()
    return fig

def get_confusion_matrix_plot(cm, title):
    set_style()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False, 
                xticklabels=['Low Risk', 'High Risk'], yticklabels=['Low Risk', 'High Risk'])
    ax.set_title(title, fontsize=12, color='white')
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    fig.tight_layout()
    return fig
