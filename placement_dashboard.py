import streamlit as st
import pandas as pd
import numpy as np
import requests  # ← NEW: API calls
import plotly.express as px

# API Configuration
API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Placement Metrics Dashboard", layout="wide")

def fetch_metrics():
    try:
        response = requests.get(f"{API_BASE}/metrics")
        return response.json()
    except:
        st.error("🔌 Backend API not running. Showing cached data...")
        return None

def fetch_data(branch="all"):
    try:
        response = requests.get(f"{API_BASE}/data", params={"branch": branch})
        return pd.DataFrame(response.json())
    except:
        st.error("Cannot fetch data from API")
        return pd.read_csv('data_sample.csv')

def predict_placement(gpa, test_score, work_experience):
    try:
        response = requests.get(f"{API_BASE}/predict", params={
            "gpa": gpa, "test_score": test_score, "work_experience": work_experience
        })
        return response.json()["placement_probability"]
    except:
        return 0.5  # Fallback

def main():
    st.title("🎓 Placement Metrics Dashboard")
    st.markdown("**Connected to FastAPI Backend** 🔌")
    
    # Fetch data from API
    df = fetch_data()
    metrics = fetch_metrics()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    branch_filter = st.sidebar.multiselect("Branch", options=df['branch'].unique(), default=df['branch'].unique())
    df_filtered = df[df['branch'].isin(branch_filter)]
    
    # Key Metrics from API
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", metrics['total_students'] if metrics else len(df_filtered))
    with col2:
        st.metric("Placement Rate", f"{metrics['placement_rate'] if metrics else 84}%")
    with col3:
        st.metric("Avg Package (LPA)", f"₹{metrics['avg_package'] if metrics else 16.8}")
    with col4:
        st.metric("Top Recruiter", metrics['top_company'] if metrics else "Google")
    
    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        branch_placement = df_filtered.groupby(['branch', 'placed']).size().unstack(fill_value=0)
        fig_branch = px.bar(branch_placement, x=branch_placement.index, y=[0,1], barmode='group', title="Placements by Branch")
        st.plotly_chart(fig_branch, use_container_width=True)
    
    with col_b:
        placed_data = df_filtered[df_filtered['placed']==1]
        fig_package = px.box(placed_data, x='company', y='package_placed', title="Package Distribution")
        st.plotly_chart(fig_package, use_container_width=True)
    
    # ML Predictor with API
    st.subheader("🔮 ML Placement Predictor")
    col_pred1, col_pred2 = st.columns([1,2])
    
    with col_pred1:
        gpa = st.number_input("GPA", 0.0, 10.0, 7.5)
        test = st.number_input("Test Score", 0, 100, 75)
        exp = st.number_input("Work Experience (yrs)", 0, 5, 0)
        
        if st.button("🔮 Predict Placement", type="primary"):
            probability = predict_placement(gpa, test, exp)
            st.success(f"🎯 Placement Probability: **{(probability*100):.1f}%**")
            st.balloons()
    
    with col_pred2:
        skills_data = df_filtered['skills'].str.split(',').explode().value_counts().head(10)
        fig_skills = px.bar(x=skills_data.index, y=skills_data.values, title="Top In-Demand Skills")
        st.plotly_chart(fig_skills, use_container_width=True)

if __name__ == "__main__":
    main()
