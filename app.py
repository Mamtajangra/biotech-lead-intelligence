import sys
import os


# Temporary fix for Python 3.13 compatibility issue:
# 'imghdr' module was removed in Python 3.13, but Streamlit still tries to import it.
# This creates a dummy (fake) module so Streamlit doesn't crash during impor
# import types
# sys.modules['imghdr'] = types.ModuleType('imghdr')

sys.path.append(os.path.abspath("."))  
# Current project path ko Python path me add kar rahe hain
# Taaki custom modules (pipeline folder) easily import ho sake

import pandas as pd  


import streamlit as st  


from pipeline.pipeline import run_pipeline  
# pipeline.py se run_pipeline function import kar rahe hain (data processing engine)

# Page configuration
st.set_page_config(page_title="Biotech Lead Intelligence", layout="wide")  
# Page title set kiya + wide layout use kiya (table ke liye zyada space)

# Title and description
st.title(" Biotech Lead Intelligence Dashboard")  
# Dashboard ka main heading

st.caption("Identify & rank high-intent biotech leads using multi-source data")  
# Short description (app kya karta hai)

# Cache for performance
@st.cache_data
def get_data():
    return run_pipeline()  
    # Pipeline run karke final dataframe return karta hai
    # Cache use karne se bar-bar computation nahi hota (fast performance)

df = get_data()  
# Cached data ko load kar rahe hain

# Search input
search = st.text_input("Search by name, title, company, location")  
# User se search keyword input le rahe hain

# Search filtering logic
if search:
    mask = df.astype(str).apply(
        lambda col: col.str.contains(search, case=False)
    ).any(axis=1)  
    # Har column ko string me convert karke search keyword match kar rahe hain
    # case=False → case-insensitive search
    # .any(axis=1) → agar kisi bhi column me match mile to row include karo

    filtered_df = df[mask]  
    # Filtered rows select kar rahe hain
else:
    filtered_df = df  
    # Agar search empty hai to pura data show karo

# Score filter (slider)
min_score = st.slider("Minimum Score", 0, 100, 20)  
# Slider se user minimum score select karega

filtered_df = filtered_df[filtered_df["probability_score"] >= min_score]  
# Sirf wahi rows rakho jinka score >= selected value hai

# Metrics (Top stats)
col1, col2 = st.columns(2)  
# Page ko 2 columns me divide kar rahe hain

col1.metric("Total Leads", len(df))  
# Total leads count show kar rahe hain

col2.metric("High Intent Leads (>70)", len(df[df["probability_score"] > 70]))  
# High intent leads count (score > 70)

# Data Table
st.dataframe(filtered_df, use_container_width=True)  
# Filtered data ko table format me display kar rahe hain

# Chart
st.subheader("Score Distribution")  


st.bar_chart(filtered_df["probability_score"])  


# Download button
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="ranked_biotech_leads.csv"
)  
# User CSV file download kar sakta hai filtered data ka