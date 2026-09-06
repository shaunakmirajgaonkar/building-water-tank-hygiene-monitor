from pathlib import Path
import pandas as pd
from watertank_engine import score_tanks, history_summary, REQUIRED_TANK, REQUIRED_HISTORY
BASE=Path(__file__).resolve().parents[1]

def test_required_columns():
    t=pd.read_csv(BASE/'data/sample_tank_metrics.csv'); h=pd.read_csv(BASE/'data/sample_hygiene_history.csv')
    assert set(REQUIRED_TANK).issubset(t.columns); assert set(REQUIRED_HISTORY).issubset(h.columns)

def test_scores_bounded():
    out=score_tanks(pd.read_csv(BASE/'data/sample_tank_metrics.csv'))
    assert out['hygiene_risk_score'].between(0,100).all()
    assert out['risk_level'].notna().all()

def test_history_sorted_dates():
    out=history_summary(pd.read_csv(BASE/'data/sample_hygiene_history.csv'))
    assert out['date'].is_monotonic_increasing

def test_repeated_history_ids_allowed():
    h=pd.read_csv(BASE/'data/sample_hygiene_history.csv')
    assert h['tank_id'].duplicated().any()
