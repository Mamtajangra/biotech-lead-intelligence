# pipeline/pipeline.py

from pipeline.data_loader import load_data
from pipeline.processor import merge_data
from pipeline.scoring import apply_scoring

def run_pipeline():
    linkedin_df, pubmed_df, conference_df = load_data()

    df = merge_data(linkedin_df, pubmed_df, conference_df)

    df = apply_scoring(df)

    final_df = df[[
        "rank",
        "probability_score",
        "name",
        "title",
        "company",
        "person_location",
        "conference",
        "paper_title",
        "linkedin_url"
    ]]

    return final_df