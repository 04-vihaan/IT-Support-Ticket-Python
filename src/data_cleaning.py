from pathlib import Path
import pandas as pd
from data_loader import load_raw_tickets


def clean_ticket_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans raw ticket data by stripping string whitespace, removing duplicate

    IDs, and handling missing priority records.

    Args:
        df (pd.DataFrame): Input raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame copy.
    """
    cleaned_df = df.copy()

    # 1. Trim whitespace from object/string fields (e.g., Department)
    string_cols = cleaned_df.select_dtypes(include=["object"]).columns
    for col in string_cols:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

    # 2. Deduplicate records based on unique Ticket_ID
    initial_count = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["Ticket_ID"], keep="first")
    duplicates_removed = initial_count - len(cleaned_df)

    # 3. Handle missing values in Priority column
    missing_priorities = (cleaned_df["Priority"] == "None").sum() + cleaned_df[
        "Priority"
    ].isna().sum()
    cleaned_df["Priority"] = cleaned_df["Priority"].replace(
        {"None": "Unassigned", None: "Unassigned"}
    )

    print(
        f"[CLEANING COMPLETE]\n"
        f" - Duplicates removed: {duplicates_removed}\n"
        f" - Missing priorities filled: {missing_priorities}\n"
        f" - Whitespace trimmed across {len(string_cols)} text columns."
    )

    return cleaned_df


def save_cleaned_tickets(df: pd.DataFrame, output_path: str) -> None:
    """Saves processed DataFrame to CSV, ensuring parent directories exist.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        output_path (str): Target output file path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[SUCCESS] Cleaned dataset saved to '{path}'.")


if __name__ == "__main__":
    raw_path = "data/raw/it_support_tickets.csv"
    processed_path = "data/processed/cleaned_tickets.csv"

    print("Testing data_cleaning.py standalone...")
    raw_df = load_raw_tickets(raw_path)
    cleaned_df = clean_ticket_data(raw_df)
    save_cleaned_tickets(cleaned_df, processed_path)