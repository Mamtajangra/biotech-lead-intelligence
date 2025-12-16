import streamlit as st
from scoring import final_df   ## final dataframe i have created 

st.set_page_config(page_title="Biotech Lead Intelligence",layout="wide" )           ## wide = table need more space)

st.title("Biotech Lead Intelligence Dashboard")
st.caption("Identification, enrichment, and propensity scoring of high-intent leads "
    "for 3D in-vitro models")    

search = st.text_input("Search by name, title, company, location, or keyword")  ## we can  search in this manner

if search:
    filtered_df = final_df[final_df.apply(lambda x: search.lower() in str(x).lower(), axis=1)]   ## created each row string and check the ord user if that word is present here give row otherwise hide it
else:
    filtered_df = final_df

st.dataframe(filtered_df, use_container_width=True)   ## show data 

st.download_button(        ## a button appear it gives the download csv 
    label="Download Ranked Leads (CSV)",
    data=filtered_df.to_csv(index=False),
    file_name="ranked_biotech_leads.csv",
)
