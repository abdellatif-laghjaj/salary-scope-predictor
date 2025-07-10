import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

print("Starting asset preparation...")

# --- 1. Load and Clean Data (condensed from your notebook) ---
df = pd.read_csv("data/survey_results_public.csv")

# Select and rename columns
relevant_columns = [
    "Country",
    "EdLevel",
    "YearsCodePro",
    "Employment",
    "ConvertedCompYearly",
]
df_selected = df[relevant_columns].copy()
df_selected = df_selected.rename({"ConvertedCompYearly": "Salary"}, axis=1)

# Filter for full-time employment and valid salary
df_clean = df_selected[
    (df_selected["Salary"].notnull())
    & (df_selected["Employment"] == "Employed, full-time")
].copy()
df_clean = df_clean.drop("Employment", axis=1)

# Remove salary outliers
Q1 = df_clean["Salary"].quantile(0.25)
Q3 = df_clean["Salary"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = max(Q1 - 2.5 * IQR, 10000)
upper_bound = min(Q3 + 2.5 * IQR, 500000)
df_clean = df_clean[
    (df_clean["Salary"] >= lower_bound) & (df_clean["Salary"] <= upper_bound)
]

# Group rare countries into 'Other'
country_counts = df_clean["Country"].value_counts()
country_map = {
    cat: cat if count >= 300 else "Other" for cat, count in country_counts.items()
}
df_clean["Country"] = df_clean["Country"].map(country_map)
df_clean = df_clean[df_clean["Country"] != "Other"]


# Clean YearsCodePro
def clean_experience(x):
    if pd.isna(x):
        return np.nan
    if "More than 50 years" in str(x):
        return 50
    if "Less than 1 year" in str(x):
        return 0.5
    try:
        return float(x)
    except:
        return np.nan


df_clean["YearsCodePro"] = df_clean["YearsCodePro"].apply(clean_experience)


# Clean EdLevel
def clean_education(x):
    if pd.isna(x):
        return "Unknown"
    x = str(x).lower()
    if "bachelor" in x:
        return "Bachelor's degree"
    if "master" in x:
        return "Master's degree"
    if "doctoral" in x or "phd" in x:
        return "Doctoral degree"
    if "professional" in x:
        return "Professional degree"
    if "associate" in x:
        return "Associate degree"
    if "high school" in x or "secondary" in x:
        return "High school"
    return "Other/Some college"


df_clean["EdLevel"] = df_clean["EdLevel"].apply(clean_education)

# Drop remaining NaNs
df_clean = df_clean.dropna()
print(f"Data cleaned. Final shape for training: {df_clean.shape}")

# --- 2. Save the Cleaned Data for the Explore Page ---
df_clean.to_csv("cleaned_data.csv", index=False)
print("Saved cleaned_data.csv")
