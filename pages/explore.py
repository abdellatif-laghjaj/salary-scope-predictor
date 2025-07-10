import streamlit as st
import pandas as pd
import plotly.express as px


# --- Function to load the cleaned data ---
@st.cache_data
def load_data():
    """Loads the cleaned survey data."""
    try:
        df = pd.read_csv("cleaned_data.csv")
        return df
    except FileNotFoundError:
        st.error("Cleaned data file not found. Please run 'prepare_assets.py' first.")
        return None


# --- Load Data ---
df = load_data()

if df is not None:
    # --- Page Configuration ---
    st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

    # --- Page Title ---
    st.title("📊 Explore the Survey Data")
    st.markdown(
        "This page allows you to explore the cleaned dataset that was used to train the salary prediction model."
    )

    # --- Show Raw Data ---
    with st.expander("View the Raw Data"):
        st.dataframe(df)

    # --- Data Visualizations ---
    st.header("Visual Analysis")

    # --- Country Analysis ---
    st.subheader("Analysis by Country")

    # Chart 1: Number of Respondents by Country
    fig1 = px.bar(
        df["Country"].value_counts(),
        x=df["Country"].value_counts().index,
        y=df["Country"].value_counts().values,
        labels={"x": "Country", "y": "Number of Respondents"},
        title="Number of Survey Respondents by Country",
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Median Salary by Country
    salary_by_country = (
        df.groupby("Country")["Salary"].median().sort_values(ascending=False)
    )
    fig2 = px.bar(
        salary_by_country,
        x=salary_by_country.index,
        y=salary_by_country.values,
        labels={"x": "Country", "y": "Median Salary (USD)"},
        title="Median Salary by Country",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Experience Analysis ---
    st.subheader("Analysis by Experience")

    # Chart 3: Median Salary by Years of Experience
    salary_by_exp = df.groupby("YearsCodePro")["Salary"].median().sort_index()
    fig3 = px.line(
        salary_by_exp,
        x=salary_by_exp.index,
        y=salary_by_exp.values,
        labels={"x": "Years of Professional Experience", "y": "Median Salary (USD)"},
        title="Median Salary vs. Years of Experience",
        markers=True,
    )
    st.plotly_chart(fig3, use_container_width=True)

    # --- Education Analysis ---
    st.subheader("Analysis by Education Level")

    # Chart 4: Salary Distribution by Education Level
    fig4 = px.box(
        df,
        x="Salary",
        y="EdLevel",
        labels={"Salary": "Annual Salary (USD)", "EdLevel": "Education Level"},
        title="Salary Distribution by Education Level",
        orientation="h",  # Horizontal box plot
    )
    fig4.update_layout(yaxis={"categoryorder": "total ascending"})  # Sort by median
    st.plotly_chart(fig4, use_container_width=True)
