import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    aux_df = aux_df.rename(columns = {"name": "matched_name"}) #new column names
    merge = anon_df.merge(aux_df, on = ["age", "zip3", "gender"])
    counts = merge.groupby("anon_id")["matched_name"].transform("count") #count of how many names matched id's
    unique = merge[counts == 1] 

    return unique[["anon_id", "matched_name"]]#returning only matched records


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)
