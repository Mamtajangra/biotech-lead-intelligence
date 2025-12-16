import pandas as pd
linkedin_df = pd.read_csv("data/linkedin_leads.csv")
pubmed_df = pd.read_csv("data/pubmed_authors.csv")
conference_df = pd.read_csv("data/conference_leads.csv")
''' – 1..LinkedIn list (MAIN LIST)
Isme likha hai:
Naam,Job,Company,Location
2..pubmed list(Isme likha hai):
Kisne scientific paper likha,Kis topic pe,Kab
3..conference list(isme likha hai)
Kaun conference me gaya,Kis topic pe bola'''
# linkedin_df is base LinkedIn list = LEFT SIDE , PubMed list = RIGHT SIDE , Match karo → name column se
'''how="left" ka matlab:
LinkedIn wale saare log rakhna, chahe PubMed me unka naam mile ya na mile.
Result:
Jiska paper hai → paper title aa jaayega
Jiska paper nahi hai → NaN aa jaayega
Business logic:
Paper na hone ka matlab ye nahi ki banda useless hai,bas uska score kam hoga.'''
df = linkedin_df.merge(pubmed_df,on="name",how="left")
# now add the info of conference in modified list with linkedin and pubmed
# if we did not use left then it would remove all the names having not publish paper
df = df.merge(conference_df,on="name",how="left")
print(linkedin_df)
print(pubmed_df)
print(conference_df)
# Scoring logic (Business-first)
def calculate_probability_score(row):  ## through this function i will use each scientist as input and return its score
    score = 0       ## assume person is not interested

    # Role fit (decision power)
    if any(x in row["title"] for x in ["Director", "Head", "VP"]): ## if in title there is director,head,vp then we will give score 30
        score += 30

    # Scientific intent
    if pd.notna(row["paper_title"]):  ## if paper title is not empty means someone publish paper  give them score 40
        score += 40

    # Conference / active market signal
    if pd.notna(row["conference"]):   ## here check the person attend conference or not if yes give score 20
        score += 20

    # Biotech hub
    biotech_hubs = ["Boston", "Cambridge", "San Francisco", "Basel", "San Diego"]   ## if person in biotech city then give score 10
    if row["person_location"] in biotech_hubs:
        score += 10

    return score

# Apply scoring
df["probability_score"] = df.apply(calculate_probability_score, axis=1)    ## new column created and each get score
print(df)

# Rank leads
df = df.sort_values(by="probability_score", ascending=False).reset_index(drop=True)  ## sort so that high score is in upper and low score in lower
df["rank"] = df.index + 1      ## top scientist got rank 1 and so on

# Final output
final_df = df[["rank","probability_score","name","title","company","person_location","conference","paper_title",
               "linkedin_url",]]

print(final_df)