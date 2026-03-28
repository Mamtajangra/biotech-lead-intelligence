import pandas as pd

def load_data():
    linkedin_df = pd.read_csv("data/linkedin_leads.csv")
    pubmed_df = pd.read_csv("data/pubmed_authors.csv")
    conference_df = pd.read_csv("data/conference_leads.csv")

    return linkedin_df, pubmed_df, conference_df

''' – 1..LinkedIn list (MAIN LIST)
Isme likha hai:
Naam,Job,Company,Location
2..pubmed list(Isme likha hai):
Kisne scientific paper likha,Kis topic pe,Kab
3..conference list(isme likha hai)
Kaun conference me gaya,Kis topic pe bola'''