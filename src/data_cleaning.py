import pandas as pd
from pathlib import Path

def clean_ticket_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans ticket data by dropping duplicates, stripping whitespace, and filling missing priorities."""
    cleaned_df = df.copy()
    
    initial_rows = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["Ticket_ID"])
    duplicates_removed = initial_rows - len(cleaned_df)
    
    string_cols = cleaned_df.select_dtypes(include=["object", "string"]).columns
    for col in string_cols:
        cleaned_df[col] = cleaned_df[col].str.strip()
        
    missing_priorities = cleaned_df["Priority"].isna().sum()
    cleaned_df["Priority"] = cleaned_df["Priority"].fillna("Unassigned")
    
    print("Cleaning complete:")
    print(f" - Duplicates removed: {duplicates_removed}")
    print(f" - Missing priorities filled: {missing_priorities}")
    print(f" - Whitespace trimmed across {len(string_cols)} text columns.")
    
    return cleaned_df

def save_cleaned_tickets(df: pd.DataFrame, output_path: str) -> None:
    """Saves the cleaned DataFrame to a CSV file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned dataset saved to '{path}'.")