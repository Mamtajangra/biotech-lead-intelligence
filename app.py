import sys
import os
sys.path.append(os.path.abspath("."))


import pandas as pd

import streamlit as st
from pipeline.pipeline import run_pipeline

st.set_page_config(page_title="Biotech Lead Intelligence", layout="wide")             ## wide = table need more space)

st.title(" Biotech Lead Intelligence Dashboard")
st.caption("Identify & rank high-intent biotech leads using multi-source data")

#  Cache for performance
@st.cache_data
def get_data():
    return run_pipeline()

df = get_data()

#  Search
search = st.text_input("Search by name, title, company, location")

if search:
    mask = df.astype(str).apply(
        lambda col: col.str.contains(search, case=False)
    ).any(axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

# Score Filter
min_score = st.slider("Minimum Score", 0, 100, 20)
filtered_df = filtered_df[filtered_df["probability_score"] >= min_score]

#  Metrics
col1, col2 = st.columns(2)
col1.metric("Total Leads", len(df))
col2.metric("High Intent Leads (>70)", len(df[df["probability_score"] > 70]))

#  Data Table
st.dataframe(filtered_df, use_container_width=True)

#  Chart
st.subheader("Score Distribution")
st.bar_chart(filtered_df["probability_score"])

# Download
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="ranked_biotech_leads.csv"
)