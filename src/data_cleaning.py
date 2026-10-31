import pandas as pd
from pathlib import Path

def clean_ticket_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.copy()
    
    # Calculate duplicates before dropping
    initial_rows = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["Ticket_ID"])
    duplicates_removed = initial_rows - len(cleaned_df)
    
    # Strip whitespace without breaking NaNs
    string_cols = cleaned_df.select_dtypes(include=["object", "string"]).columns
    for col in string_cols:
        cleaned_df[col] = cleaned_df[col].str.strip()
        
    # Checkjng for missing priorities BEFORE filling them
    missing_priorities = cleaned_df["Priority"].isna().sum()
    print(f"Missing priorities found: {missing_priorities}")

    # Filling missing priorities
    cleaned_df["Priority"] = cleaned_df["Priority"].fillna("Unassigned")
    
    print(
        f"Cleaning Complete:\n"
        f" - Duplicates removed: {duplicates_removed}\n"
        f" - Missing priorities filled: {missing_priorities}\n"
        f" - Whitespace trimmed across {len(string_cols)} text columns."
    )
    
    return cleaned_df

def save_cleaned_tickets(df: pd.DataFrame, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned dataset saved to '{path}'.")