from __future__ import annotations
import pandas as pd
import numpy as np

REQUIRED_TANK = [
    'tank_id','tank_name','zone','latitude','longitude','tank_type','capacity_l',
    'current_level_pct','days_since_cleaning','turbidity_ntu','tds_ppm','ph',
    'bacterial_risk_index','overflow_events_30d','maintenance_overdue_days',
    'usage_lpd','condition_score'
]
REQUIRED_HISTORY = [
    'tank_id','date','level_pct','turbidity_ntu','tds_ppm','ph',
    'bacterial_risk_index','usage_lpd','overflow_events'
]

def validate_columns(df: pd.DataFrame, required: list[str], label: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing required column(s): {', '.join(missing)}")

def _clip(s, lo=0.0, hi=100.0):
    return pd.to_numeric(s, errors='coerce').fillna(0).clip(lo, hi)

def score_tanks(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, REQUIRED_TANK, 'Tank metrics CSV')
    out = df.copy()
    numeric = [c for c in REQUIRED_TANK if c not in {'tank_id','tank_name','zone','tank_type'}]
    for c in numeric:
        out[c] = pd.to_numeric(out[c], errors='coerce')
    # Explainable hygienic-risk components
    cleaning = np.clip(out['days_since_cleaning'].fillna(0) / 180 * 100, 0, 100)
    bacterial = _clip(out['bacterial_risk_index'])
    turb = np.clip(out['turbidity_ntu'].fillna(0) / 10 * 100, 0, 100)
    ph = np.clip((6.5 - out['ph'].fillna(7.0)).abs() / 1.5 * 100, 0, 100)
    tds = np.clip(out['tds_ppm'].fillna(0) / 1000 * 100, 0, 100)
    overflow = np.clip(out['overflow_events_30d'].fillna(0) / 5 * 100, 0, 100)
    maint = np.clip(out['maintenance_overdue_days'].fillna(0) / 90 * 100, 0, 100)
    condition = 100 - _clip(out['condition_score'])
    level = np.clip((out['current_level_pct'].fillna(0) - 92) / 8 * 100, 0, 100)
    score = (0.25*cleaning + 0.22*bacterial + 0.14*turb + 0.10*ph + 0.08*tds + 0.08*overflow + 0.06*maint + 0.04*condition + 0.03*level)
    out['hygiene_risk_score'] = np.round(score.clip(0,100),1)
    out['risk_level'] = pd.cut(out['hygiene_risk_score'], bins=[-0.01,24.99,49.99,74.99,100], labels=['Low','Moderate','High','Critical'])
    out['priority'] = pd.Categorical(out['risk_level'], categories=['Critical','High','Moderate','Low'], ordered=True)
    comp = pd.DataFrame({
        'Cleaning overdue':cleaning,'Bacterial risk':bacterial,'Turbidity':turb,
        'pH deviation':ph,'TDS':tds,'Overflow':overflow,'Maintenance':maint,
        'Condition':condition,'High storage':level
    })
    out['top_driver'] = comp.idxmax(axis=1)
    out['storage_level_l'] = (out['capacity_l'].fillna(0)*out['current_level_pct'].fillna(0)/100).round(0)
    out['daily_turnover_pct'] = np.where(out['capacity_l']>0, out['usage_lpd']/out['capacity_l']*100, 0).round(1)
    return out

def history_summary(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, REQUIRED_HISTORY, 'Performance history CSV')
    out = df.copy()
    out['date'] = pd.to_datetime(out['date'], errors='coerce')
    for c in REQUIRED_HISTORY[2:]:
        out[c] = pd.to_numeric(out[c], errors='coerce')
    return out.dropna(subset=['date']).sort_values('date')

def classify(score: float) -> str:
    if score >= 75: return 'Critical'
    if score >= 50: return 'High'
    if score >= 25: return 'Moderate'
    return 'Low'
