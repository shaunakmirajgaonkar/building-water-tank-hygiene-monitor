# WaterTankCare — Building Water-Tank Hygiene Monitor

Privacy-conscious, local-first screening and maintenance-planning dashboard for shared residential and public water tanks.

## Features
- Explainable 0–100 hygiene-risk screening score
- Low / Moderate / High / Critical classification
- Cleaning-overdue, bacterial-risk, turbidity, pH, TDS, overflow and maintenance analytics
- Tank explorer, maintenance planner, historical trends and scenario simulator
- Local CSV upload with schema validation
- CSV report exports
- Responsive colorful Streamlit UI
- No external APIs or cloud databases

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 validate_project.py
python3 -m pytest -q
python3 run.py
```

## Responsible use
This project is a screening and operational planning aid. It does not certify water quality, potability, contamination status, cleaning completion, tank integrity, or regulatory compliance. Field inspection and appropriate water testing remain necessary.
