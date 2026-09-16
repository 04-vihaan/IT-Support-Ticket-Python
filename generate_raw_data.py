from pathlib import Path
import numpy as np
import pandas as pd

# Set seed for reproducible realistic data
np.random.seed(42)
n_rows = 10000

ticket_ids = [f"TCK-{1000 + i}" for i in range(n_rows)]

# Department SLA multipliers (in hours) to simulate real-world variance
dept_sla_mean = {
    "IT Support": 8.5,  # Quick turnarounds (resets, peripherals)
    "HR": 14.2,  # Moderate policy/payroll queries
    "Operations": 18.0,  # Standard operational workflows
    "Finance": 24.5,  # Longer processing for approvals
    "DevOps": 31.0,  # Complex infrastructure/deployment issues
}

departments = list(dept_sla_mean.keys())
chosen_depts = np.random.choice(
    departments, size=n_rows, p=[0.30, 0.20, 0.20, 0.15, 0.15]
)

# Generate timestamps
start_date = pd.Timestamp("2025-01-01")
created_offsets = np.random.uniform(0, 180 * 24 * 3600, size=n_rows)
created_dates = [start_date + pd.Timedelta(seconds=s) for s in created_offsets]

# Generate resolution dates based on department-specific log-normal distributions
resolved_dates = []
for created, dept in zip(created_dates, chosen_depts):
    mean_hours = dept_sla_mean[dept]
    # Log-normal creates realistic long-tail resolution times (some quick, few long outages)
    duration_hours = np.random.lognormal(
        mean=np.log(mean_hours), sigma=0.5
    )
    resolved_dates.append(created + pd.Timedelta(hours=duration_hours))

priorities = np.random.choice(
    ["Low", "Medium", "High", "Critical", "None"],
    size=n_rows,
    p=[0.35, 0.35, 0.18, 0.07, 0.05],
)
categories = np.random.choice(
    ["Software", "Hardware", "Network", "Access", "Database"], size=n_rows
)
statuses = np.random.choice(["Closed", "Resolved"], size=n_rows, p=[0.7, 0.3])

# Introduce dirty data for the cleaning module to catch
dept_dirty = [
    f"  {d} " if i % 12 == 0 else d for i, d in enumerate(chosen_depts)
]

df = pd.DataFrame(
    {
        "Ticket_ID": ticket_ids,
        "Created_Date": created_dates,
        "Resolved_Date": resolved_dates,
        "Priority": priorities,
        "Department": dept_dirty,
        "Category": categories,
        "Status": statuses,
    }
)

# Inject duplicates for cleaning module validation
df.iloc[15] = df.iloc[14]

# Save output
raw_path = Path("data/raw/it_support_tickets.csv")
raw_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(raw_path, index=False)
print(f"[SUCCESS] Regenerated realistic raw ticket dataset at '{raw_path}'")