import pandas as pd
# Scoring logic (Business-first)
def calculate_probability_score(row):  ## through this function i will use each scientist as input and return its score
     # Ye function har row (scientist) ko input leta hai aur uska score calculate karta hai
    score = 0       ## assume person is not interested

    title = str(row.get("title","")).lower()
        # title column ko safely fetch kar rahe hain (agar missing ho to empty string)
    # lower() use kiya taaki case-insensitive matching ho (Director = director)

    # Role fit (decision power)
    if any(x in title for x in ["director", "head", "vp"]): ## if in title there is director,head,vp then we will give score 30
            # Check kar rahe hain ki title me senior roles (Director, Head, VP) present hain ya nahi
        # any() ka matlab: agar koi bhi match mila to True

        #  Agar senior role hai to 30 score add 
        score += 30

    # Scientific intent
    if pd.notna(row.get()"paper_title")):  ## if paper title is not empty means someone publish paper  give them score 40
        # Check kar rahe hain ki paper_title null nahi hai (person ne research publish kiya hai)
        # Research publish kiya → high intent → 40 score add
        score += 40

    # Conference / active market signal
    if pd.notna(row.get()"conference")):   ## here check the person attend conference or not if yes give score 20
          # Check kar rahe hain ki person conference attend/speak kiya hai ya nahi
           # Conference participation → active in field → 20 score add
        score += 20

    # Biotech hub
    biotech_hubs = ["boston", "cambridge", "san francisco", "basel", "san diego"]   ## if person in biotech city then give score 10
     # Ye list top biotech cities ki hai (high industry activity zones)
    location = str(row.get("person_location","")).lower()
     # person_location safely fetch kiya aur lowercase me convert kiya
    
    if  location in biotech_hubs:
         # Check kar rahe hain ki person biotech hub me hai ya nahi
 # Agar biotech hub me hai to 10 score add (better opportunity zone)
        score += 10

    return score

# Apply scoring

def apply_scoring(df):
     # Ye function pura dataframe leta hai aur scoring apply karta hai
    df["probability_score"] = df.apply(calculate_probability_score, axis=1)    ## new column created and each get score
       # Har row pe scoring function apply kar rahe hain
    # axis=1 → row-wise apply
    # New column "probability_score" create ho raha hai
    
    print(df)
    # Debug purpose: dataframe print kar rahe hain (production me remove karna chahiye)

# Rank leads
    df = df.sort_values(by="probability_score", ascending=False).reset_index(drop=True)  ## sort so that high score is in upper and low score in lower
      # Data ko score ke basis pe sort kiya (highest score upar)
    # reset_index → index ko clean reset kar diya
    
    df["rank"] = df.index + 1      ## top scientist got rank 1 and so on
       # Rank assign kar rahe hain (top lead = rank 1)
    return df
 # Final processed dataframe return kar rahe hain

