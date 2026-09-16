# IT Support Ticket Management & Resolution Analytics

A modular Python pipeline for ingesting, cleaning, analyzing, and reporting on IT support ticket logs using standard data libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`).

## Project Architecture

```plaintext
IT-Support-Ticket-Python/
│
├── data/
│   ├── raw/                      # Raw CSV ticket export (~10,000 rows)
│   └── processed/                # Sanitized output CSV
├── src/
│   ├── __init__.py               # Package marker
│   ├── data_loader.py            # File I/O & exception handling
│   ├── data_cleaning.py          # String sanitization & deduplication
│   ├── ticket_analysis.py        # Datetime math & SLA performance binning
│   └── visualization.py         # Plotting & image generation
├── reports/                      # Exported PNG chart assets
├── main.py                       # Single-command pipeline orchestrator
├── requirements.txt              # Project dependencies
└── README.md