from pathlib import Path
import pandas as pd
from watertank_engine import REQUIRED_TANK, REQUIRED_HISTORY, score_tanks, history_summary
BASE=Path(__file__).resolve().parent

def main():
    tanks=pd.read_csv(BASE/'data/sample_tank_metrics.csv')
    hist=pd.read_csv(BASE/'data/sample_hygiene_history.csv')
    scored=score_tanks(tanks)
    history_summary(hist)
    print('PASS: WaterTankCare building water-tank hygiene screening')
    print(f'Tanks: {len(tanks)}')
    print(f'History rows: {len(hist)}')
    print(f'Risk range: {scored.hygiene_risk_score.min():.1f}-{scored.hygiene_risk_score.max():.1f}')
    print(f'High/Critical: {int(scored.risk_level.isin(["High","Critical"]).sum())}')
if __name__=='__main__': main()
