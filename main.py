import sys
from pathlib import Path

# Add 'src' directory to Python's search path so sub-modules can import each other
sys.path.append(str(Path(__file__).parent / "src"))

from data_loader import load_raw_tickets
from data_cleaning import clean_ticket_data
from ticket_analysis import process_ticket_metrics
from visualization import generate_all_plots

def main():
    print("Starting IT Support Ticket Pipeline...")

    # 1. Load Data
    raw_data_path = "data/raw/it_support_tickets.csv"
    print(f"Loading data from {raw_data_path}...")
    df = load_raw_tickets(raw_data_path)
    
    # 2. Clean Data
    print("Cleaning ticket data...")
    cleaned_df = clean_ticket_data(df)
    
    # 3. Analyze Data
    print("Running ticket analysis...")
    analyzed_df = process_ticket_metrics(cleaned_df)
    
    # 4. Generate Visualizations
    print("Generating visualizations...")
    generate_all_plots(analyzed_df)
    
    print("Pipeline complete! Check your reports folder.")

if __name__ == "__main__":
    main()