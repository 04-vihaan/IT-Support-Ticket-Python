from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from data_cleaning import clean_ticket_data
from data_loader import load_raw_tickets
from ticket_analysis import process_ticket_metrics

# Set consistent visual aesthetic across all outputs
sns.set_theme(style="whitegrid", palette="muted")


def generate_all_plots(
    df: pd.DataFrame, output_dir: str = "reports"
) -> None:
    """Generates 3 key visual reporting assets and exports them to disk.

    Args:
        df (pd.DataFrame): Processed ticket dataset containing calculated
          metrics.
        output_dir (str): Target directory to save generated plots.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Chart 1: Ticket Volume Over Time (Weekly Aggregation)
    plt.figure(figsize=(10, 5))
    weekly_counts = (
        df.set_index("Created_Date").resample("W-MON")["Ticket_ID"].count()
    )
    sns.lineplot(
        x=weekly_counts.index,
        y=weekly_counts.values,
        marker="o",
        color="#1f77b4",
        linewidth=2.5,
    )
    plt.title("Weekly Support Ticket Inflow Volume (2025)", fontsize=14, pad=12)
    plt.xlabel("Date (Weekly Bin)", fontsize=11)
    plt.ylabel("Total Tickets Created", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path / "ticket_volume_over_time.png", dpi=300)
    plt.close()

    # Chart 2: Mean Resolution Latency by Department
    plt.figure(figsize=(9, 5))
    dept_avg = (
        df.groupby("Department")["Resolution_Time_Hours"]
        .mean()
        .reset_index()
        .sort_values(by="Resolution_Time_Hours", ascending=False)
    )
    sns.barplot(
        data=dept_avg, x="Department", y="Resolution_Time_Hours", palette="crest"
    )
    plt.title("Average Resolution Duration by Department", fontsize=14, pad=12)
    plt.xlabel("Department", fontsize=11)
    plt.ylabel("Mean Hours to Resolve", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path / "avg_resolution_by_department.png", dpi=300)
    plt.close()

    # Chart 3: Ticket Count Distribution by Priority Level
    plt.figure(figsize=(8, 5))
    priority_order = ["Critical", "High", "Medium", "Low", "Unassigned"]
    sns.countplot(
        data=df,
        x="Priority",
        order=[p for p in priority_order if p in df["Priority"].unique()],
        palette="magma",
    )
    plt.title("Ticket Distribution by Priority Level", fontsize=14, pad=12)
    plt.xlabel("Priority Class", fontsize=11)
    plt.ylabel("Ticket Count", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path / "priority_distribution.png", dpi=300)
    plt.close()

    print(
        f"[SUCCESS] Saved 3 figure files to directory: '{out_path.resolve()}'"
    )


if __name__ == "__main__":
    raw_path = "data/raw/it_support_tickets.csv"

    print("Testing visualization.py standalone...")
    raw_df = load_raw_tickets(raw_path)
    cleaned_df = clean_ticket_data(raw_df)
    analyzed_df = process_ticket_metrics(cleaned_df)

    generate_all_plots(analyzed_df, output_dir="reports")