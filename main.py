import sys
from pathlib import Path

# 1. Tell Python where to find the modules BEFORE importing them
sys.path.append(str(Path(__file__).parent / "src"))

# 2. Now we can safely import from the src folder
from data_loader import load_raw_tickets
from data_cleaning import clean_ticket_data, save_cleaned_tickets
from ticket_analysis import process_ticket_metrics
from visualization import generate_all_plots

def main():
    print("Starting IT Support Ticket Pipeline...")
    
    # 1. Load Data
    raw_data_path = "data/raw/it_support_tickets.csv"
    print(f"Loading data from {raw_data_path}...")
    raw_tickets = load_raw_tickets(raw_data_path)
    
    # 2. Clean Data
    print("Cleaning tickets...")
    cleaned_tickets = clean_ticket_data(raw_tickets)
    
    # Save the cleaned CSV so the processed folder isn't stale
    save_cleaned_tickets(cleaned_tickets, 'data/processed/cleaned_tickets.csv')
    
    # 3. Analysing Metrics
    print("Calculating metrics...")
    metrics_df = process_ticket_metrics(cleaned_tickets)
    
    # 4. Generating the Visualizations
    print("Generating visual plots...")
    generate_all_plots(metrics_df)
    
    print("Pipeline finished successfully.")

if __name__ == "__main__":
    main()