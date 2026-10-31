import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def generate_all_plots(df: pd.DataFrame, out_dir: str = "reports") -> None:
    """Generates and saves visualizations for the ticket data."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Weekly Ticket Volume
    plt.figure(figsize=(10, 5))
    weekly_vol = df.set_index(pd.to_datetime(df["Created_Date"])).resample("W-MON").size()
    sns.lineplot(x=weekly_vol.index, y=weekly_vol.values, marker="o", color="b")
    plt.title("Weekly Ticket Volume", fontsize=14, pad=12)
    plt.xlabel("Week", fontsize=11)
    plt.ylabel("Tickets Created", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_path / "weekly_volume.png", dpi=300)
    plt.close()

    # 2. Average Resolution Time by Department
    plt.figure(figsize=(10, 6))
    dept_avg = (
        df.groupby("Department")["Resolution_Time_Hours"]
        .mean()
        .reset_index()
        .sort_values(by="Resolution_Time_Hours", ascending=False)
    )
    sns.barplot(
        data=dept_avg, x="Department", y="Resolution_Time_Hours", hue="Department", legend=False, palette="viridis"
    )
    plt.title("Average Resolution Duration by Department", fontsize=14, pad=12)
    plt.xlabel("Department", fontsize=11)
    plt.ylabel("Mean Hours to Resolve", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path / "avg_resolution_by_department.png", dpi=300)
    plt.close()

    # 3. Ticket Count by Priority
    plt.figure(figsize=(8, 5))
    priority_order = ["Critical", "High", "Medium", "Low", "Unassigned"]
    sns.countplot(
        data=df,
        x="Priority",
        order=[p for p in priority_order if p in df["Priority"].unique()],
        hue="Priority", legend=False, palette="viridis"
    )
    plt.title("Ticket Distribution by Priority Level", fontsize=14, pad=12)
    plt.xlabel("Priority", fontsize=11)
    plt.ylabel("Ticket Count", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path / "priority_distribution.png", dpi=300)
    plt.close()

    print(f"Visualizations successfully saved to '{out_path}'.")