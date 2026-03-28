

def merge_data(linkedin_df, pubmed_df, conference_df):
    df = linkedin_df.merge(pubmed_df, on="name", how="left")

    # now add the info of conference in modified list with linkedin and pubmed
# if we did not use left then it would remove all the names having not publish paper
    df = df.merge(conference_df, on="name", how="left")


    return df

# linkedin_df is base LinkedIn list = LEFT SIDE , PubMed list = RIGHT SIDE , Match karo → name column se
'''how="left" ka matlab:
LinkedIn wale saare log rakhna, chahe PubMed me unka naam mile ya na mile.
Result:
Jiska paper hai → paper title aa jaayega
Jiska paper nahi hai → NaN aa jaayega
Business logic:
Paper na hone ka matlab ye nahi ki banda useless hai,bas uska score kam hoga.'''