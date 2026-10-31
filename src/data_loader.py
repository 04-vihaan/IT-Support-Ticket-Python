import pandas as pd
from pathlib import Path

def load_raw_tickets(file_path: str) -> pd.DataFrame:
    """Loads raw ticket data from a CSV file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found at {path}")
        
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("The dataset is empty.")
        
    print(f"Data loaded: {len(df)} records found in {path.name}.")
    return df