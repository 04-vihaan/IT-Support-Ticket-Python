import numpy as np
import pandas as pd
from data_cleaning import clean_ticket_data
from data_loader import load_raw_tickets


def process_ticket_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Parses datetime strings, calculates resolution durations in hours,

    and assigns performance SLA categories using numpy condition arrays.

    Args:
        df (pd.DataFrame): Cleaned ticket dataset.

    Returns:
        pd.DataFrame: DataFrame populated with resolution analysis fields.
    """
    analyzed_df = df.copy()

    # 1. Parse string timestamps into native pandas datetime objects
    analyzed_df["Created_Date"] = pd.to_datetime(analyzed_df["Created_Date"])
    analyzed_df["Resolved_Date"] = pd.to_datetime(analyzed_df["Resolved_Date"])

    # 2. Compute exact resolution latency in decimal hours
    time_diff = analyzed_df["Resolved_Date"] - analyzed_df["Created_Date"]
    analyzed_df["Resolution_Time_Hours"] = (
        time_diff.dt.total_seconds() / 3600.0
    ).round(2)

    # 3. Classify response speed into performance buckets with np.select
    conditions = [
        analyzed_df["Resolution_Time_Hours"] < 4.0,
        (analyzed_df["Resolution_Time_Hours"] >= 4.0)
        & (analyzed_df["Resolution_Time_Hours"] <= 24.0),
        analyzed_df["Resolution_Time_Hours"] > 24.0,
    ]
    choices = ["Fast (<4h)", "Normal (4-24h)", "Delayed (>24h)"]

    analyzed_df["Performance_Bucket"] = np.select(
        conditions, choices, default="Unknown"
    )

    print(
        "[ANALYSIS COMPLETE] Calculated 'Resolution_Time_Hours' and assigned 'Performance_Bucket'."
    )
    return analyzed_df


if __name__ == "__main__":
    raw_path = "data/raw/it_support_tickets.csv"

    print("Testing ticket_analysis.py standalone...")
    raw_df = load_raw_tickets(raw_path)
    cleaned_df = clean_ticket_data(raw_df)
    analyzed_df = process_ticket_metrics(cleaned_df)

    print("\nSample Analyzed Metrics:")
    print(
        analyzed_df[
            [
                "Ticket_ID",
                "Department",
                "Resolution_Time_Hours",
                "Performance_Bucket",
            ]
        ].head(5)
    )