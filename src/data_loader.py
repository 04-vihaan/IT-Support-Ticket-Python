from pathlib import Path
import pandas as pd


def load_raw_tickets(file_path: str) -> pd.DataFrame:
    """Safely loads raw IT support ticket CSV data into a pandas DataFrame.

    Args:
        file_path (str): Relative or absolute path to the raw CSV file.

    Returns:
        pd.DataFrame: Loaded raw ticket dataset.
    """
    path = Path(file_path)

    # Check file existence using pathlib
    if not path.is_file():
        raise FileNotFoundError(
            f"[IO Error] Target file not found: {path.resolve()}"
        )

    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(
                f"[Data Error] File exists but contains no data: {path}"
            )

        print(
            f"[SUCCESS] Loaded {len(df):,} records across {len(df.columns)} columns from '{path.name}'."
        )
        return df

    except pd.errors.EmptyDataError:
        print(f"[ERROR] Dataset at '{path}' is completely blank.")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error while loading '{path}': {e}")
        raise


if __name__ == "__main__":
    # Internal module testing
    test_path = "data/raw/it_support_tickets.csv"
    print("Testing data_loader.py execution...")
    raw_df = load_raw_tickets(test_path)
    print("\nDataset Preview:")
    print(raw_df.head(3))