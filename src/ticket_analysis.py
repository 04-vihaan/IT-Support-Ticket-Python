import pandas as pd
import numpy as np

def process_ticket_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates resolution time in hours and assigns performance buckets."""
    analyzed_df = df.copy()

    # 1. Parse string timestamps into native pandas datetime objects
    analyzed_df["Created_Date"] = pd.to_datetime(analyzed_df["Created_Date"])
    analyzed_df["Resolved_Date"] = pd.to_datetime(analyzed_df["Resolved_Date"])

    # 2. Computing exact resolution latency in decimal hours
    time_diff = analyzed_df["Resolved_Date"] - analyzed_df["Created_Date"]
    analyzed_df["Resolution_Time_Hours"] = (time_diff.dt.total_seconds() / 3600.0).round(2)

    # 3. Assigning the pwrformance Buckets
    conditions = [
        (analyzed_df["Resolution_Time_Hours"] < 4),
        (analyzed_df["Resolution_Time_Hours"] >= 4) & (analyzed_df["Resolution_Time_Hours"] <= 24),
        (analyzed_df["Resolution_Time_Hours"] > 24)
    ]
    choices = ["<4h", "4-24h", ">24h"]
    analyzed_df["Performance_Bucket"] = np.select(conditions, choices, default="Unknown")

    print("Added Resolution_Time_Hours and Performance_Bucket.")
    return analyzed_df