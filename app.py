from __future__ import annotations
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from watertank_engine import REQUIRED_TANK, REQUIRED_HISTORY, score_tanks, history_summary, classify

st.set_page_config(page_title='WaterTankCare | Building Water-Tank Hygiene Monitor', page_icon='💧', layout='wide', initial_sidebar_state='expanded')

BASE = Path(__file__).resolve().parent
DATA = BASE/'data'
ASSETS = BASE/'assets'

CSS = """
<style>
:root{--navy:#123b6d;--blue:#1787ea;--teal:#17a889;--green:#22b573;--orange:#f59e0b;--red:#e94f64;--purple:#7c4dff;--ink:#17345f;--muted:#66809d;--line:#dceaf4;--bg:#f4faff}
.stApp{background:linear-gradient(180deg,#eef9ff 0%,#f8fcff 28%,#fbfffc 100%);color:var(--ink)}
.block-container{padding-top:1.2rem;padding-bottom:2.5rem;max-width:1500px}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#edf8ff 0%,#f6fffb 100%);border-right:1px solid #dbeaf3}
.hero{display:grid;grid-template-columns:160px minmax(0,1fr) 280px;gap:22px;align-items:center;background:linear-gradient(120deg,#e5f6ff,#effff8 55%,#fffdf0);border:1px solid #d8eaf4;border-radius:28px;padding:24px 28px;box-shadow:0 18px 50px rgba(30,100,150,.10);margin-bottom:24px}
.hero-logo{display:flex;justify-content:center;align-items:center}.hero-logo img{width:128px;height:128px;object-fit:contain}
.hero-title{font-size:clamp(2rem,3.3vw,3.3rem);font-weight:850;line-height:1.08;color:#103a76;margin:0 0 8px;word-break:break-word}.hero-sub{font-size:1.08rem;color:#476b8d;margin-bottom:12px}.badges{display:flex;flex-wrap:wrap;gap:8px}.badge{padding:8px 12px;border-radius:999px;background:#fff;border:1px solid #dcebf4;color:#25537e;font-weight:700;font-size:.82rem}.callout{background:rgba(255,255,255,.78);border:1px solid #d7eadf;border-radius:20px;padding:20px}.callout b{display:block;color:#0d6d55;font-size:1.02rem;margin-bottom:8px}.callout span{color:#59758e;font-size:.9rem}
.section-title{font-size:2rem;font-weight:800;color:#123b6d;margin:18px 0 4px}.section-sub{color:#6d86a0;font-size:1rem;margin-bottom:18px}
.metric-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px;margin-bottom:18px}.metric{background:#fff;border:1px solid var(--line);border-radius:20px;padding:19px;min-width:0;box-shadow:0 8px 25px rgba(37,90,130,.06)}.metric small{display:block;color:#65809a;font-weight:800;letter-spacing:.05em;font-size:.78rem;margin-bottom:10px}.metric strong{display:block;font-size:1.9rem;color:#153f78;line-height:1.1}.metric em{font-style:normal;color:#4e8c79;font-size:.86rem;margin-top:8px;display:block}
.panel{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 18px 10px;box-shadow:0 8px 25px rgba(37,90,130,.06);height:100%}.panel h3{margin:0 0 6px;color:#153d6e}.muted{color:#6d86a0}
.alert{padding:12px 14px;border-radius:14px;border:1px solid #f6d0d8;background:#fff4f6;color:#9f2742;font-weight:700;margin-bottom:10px}.good{background:#effcf6;border-color:#c9eedc;color:#147653}.warn{background:#fff9ea;border-color:#f7e2af;color:#996310}
@media (max-width:1100px){.hero{grid-template-columns:110px minmax(0,1fr)}.callout{grid-column:1/-1}.metric-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:650px){.hero{grid-template-columns:1fr;text-align:center}.hero-logo img{width:96px;height:96px}.badges{justify-content:center}.metric-grid{grid-template-columns:1fr}.hero-title{font-size:2rem}}
</style>
"""
st.markdown(CSS,unsafe_allow_html=True)

def load_default():
    tanks=pd.read_csv(DATA/'sample_tank_metrics.csv')
    hist=pd.read_csv(DATA/'sample_hygiene_history.csv')
    return score_tanks(tanks), history_summary(hist)

# correct cache decorator declaration without unsupported syntax
@st.cache_data(show_spinner=False)
def cached_default():
    tanks=pd.read_csv(DATA/'sample_tank_metrics.csv')
    hist=pd.read_csv(DATA/'sample_hygiene_history.csv')
    return score_tanks(tanks), history_summary(hist)

scored, history = cached_default()

with st.sidebar:
    st.markdown('## 💧 WaterTankCare')
    st.caption('Building Water-Tank Hygiene Monitor')
    page=st.radio('Navigate', ['Dashboard','Risk Analysis','Tank Explorer','Maintenance Planner','Historical Trends','Scenario Simulator','Data Upload','Reports'])
    st.divider()
    st.markdown('**LOCAL-FIRST PROCESSING**')
    st.caption('CSV • Pandas • NumPy • Plotly')
    st.caption('No external APIs required')
    st.divider()
    st.markdown('**Purpose**')
    st.caption('Screen hygiene, overflow, contamination, and maintenance signals for operational review.')

logo = ASSETS/'watertankcare_logo.svg'
logo_uri = 'data:image/svg+xml;utf8,' + logo.read_text().replace('#','%23').replace('\n','')

st.markdown(f"""
<div class='hero'>
  <div class='hero-logo'><img src='{logo_uri}' alt='WaterTankCare logo'></div>
  <div>
    <h1 class='hero-title'>Building Water-Tank Hygiene Monitor</h1>
    <div class='hero-sub'>WaterTankCare • Monitor hygiene, identify risks, and plan maintenance for safer shared water systems.</div>
    <div class='badges'><span class='badge'>100% Local</span><span class='badge'>Explainable Analytics</span><span class='badge'>Hygiene Screening</span><span class='badge'>Maintenance Planning</span></div>
  </div>
  <div class='callout'><b>MONITOR • PREVENT • MAINTAIN</b><span>Clean tanks • Healthy communities • Safer tomorrow</span></div>
</div>
""",unsafe_allow_html=True)

if page=='Dashboard':
    st.markdown("<div class='section-title'>Command Center</div><div class='section-sub'>Operational overview of hygiene, contamination, overflow, storage, and maintenance signals.</div>",unsafe_allow_html=True)
    n=len(scored); high=int(scored['risk_level'].isin(['High','Critical']).sum()); overdue=int((scored['maintenance_overdue_days']>0).sum()); overflow=int((scored['overflow_events_30d']>0).sum()); avg=float(scored['hygiene_risk_score'].mean())
    total_cap=int(scored['capacity_l'].sum()); total_st=int(scored['storage_level_l'].sum())
    st.markdown(f"""<div class='metric-grid'>
    <div class='metric'><small>TOTAL TANKS</small><strong>{n}</strong><em>Across monitored zones</em></div>
    <div class='metric'><small>HIGH / CRITICAL RISK</small><strong>{high}</strong><em>{high/n*100:.1f}% of total</em></div>
    <div class='metric'><small>ADEQUATE TANKS</small><strong>{n-high}</strong><em>{(n-high)/n*100:.1f}% of total</em></div>
    <div class='metric'><small>TANKS OVERDUE</small><strong>{overdue}</strong><em>Cleaning or maintenance review</em></div>
    <div class='metric'><small>AVERAGE RISK</small><strong>{avg:.1f}/100</strong><em>Fleet screening indicator</em></div>
    </div>""",unsafe_allow_html=True)

    c1,c2,c3=st.columns([1.3,1,1.15])
    with c1:
        st.markdown("<div class='panel'><h3>Tank Locations & Risk Levels</h3>",unsafe_allow_html=True)
        fig=px.scatter_geo(scored,lat='latitude',lon='longitude',color='risk_level',hover_name='tank_name',hover_data={'hygiene_risk_score':True,'zone':True},projection='natural earth',height=360)
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='white',geo=dict(showland=True,landcolor='#eef7ef',showlakes=True,lakecolor='#dff2ff'))
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='panel'><h3>Risk Level Distribution</h3>",unsafe_allow_html=True)
        rc=scored['risk_level'].value_counts().reindex(['Low','Moderate','High','Critical']).fillna(0).reset_index(); rc.columns=['risk','count']
        fig=px.pie(rc,names='risk',values='count',hole=.58,height=300)
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='white',showlegend=True)
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
        st.markdown('</div>',unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='panel'><h3>Top Risk Tanks</h3>",unsafe_allow_html=True)
        top=scored.sort_values('hygiene_risk_score',ascending=False).head(6)[['tank_name','zone','hygiene_risk_score','risk_level','top_driver']]
        st.dataframe(top,use_container_width=True,hide_index=True,height=300)
        st.markdown('</div>',unsafe_allow_html=True)

    c4,c5,c6=st.columns([1.2,1,1])
    with c4:
        st.markdown("<div class='panel'><h3>Hygiene Indicators (Average)</h3>",unsafe_allow_html=True)
        vals=pd.DataFrame({'Indicator':['Turbidity','TDS','Bacterial risk','pH deviation'],'Value':[scored.turbidity_ntu.mean(),scored.tds_ppm.mean(),scored.bacterial_risk_index.mean(),(scored.ph-7).abs().mean()]})
        fig=px.bar(vals,x='Indicator',y='Value',height=300,text_auto='.1f')
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='white')
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
        st.markdown('</div>',unsafe_allow_html=True)
    with c5:
        st.markdown("<div class='panel'><h3>Cleaning Status</h3>",unsafe_allow_html=True)
        status=pd.Series(np.where(scored.days_since_cleaning<=90,'Cleaned',np.where(scored.days_since_cleaning<=150,'Due Soon','Overdue'))).value_counts().reindex(['Cleaned','Due Soon','Overdue']).fillna(0).reset_index(); status.columns=['status','count']
        fig=px.pie(status,names='status',values='count',hole=.58,height=300)
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='white')
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
        st.markdown('</div>',unsafe_allow_html=True)
    with c6:
        st.markdown("<div class='panel'><h3>Risk Drivers</h3>",unsafe_allow_html=True)
        drivers=scored['top_driver'].value_counts().head(7).reset_index(); drivers.columns=['driver','count']
        fig=px.bar(drivers,x='count',y='driver',orientation='h',height=300,text_auto=True)
        fig.update_layout(margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor='white',yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Recent Operational Alerts</h3>',unsafe_allow_html=True)
    alerts=scored.sort_values('hygiene_risk_score',ascending=False).head(6)
    for _,r in alerts.iterrows():
        cls='alert' if r.risk_level in ['High','Critical'] else 'warn'
        st.markdown(f"<div class='{cls}'>{r.tank_name} • {r.risk_level} • score {r.hygiene_risk_score:.1f} • primary driver: {r.top_driver}</div>",unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

elif page=='Risk Analysis':
    st.markdown("<div class='section-title'>Risk Analysis</div><div class='section-sub'>Explainable tank-level screening with visible component signals.</div>",unsafe_allow_html=True)
    tank=st.selectbox('Select tank', scored['tank_name'].tolist())
    row=scored.loc[scored.tank_name==tank].iloc[0]
    a,b,c,d=st.columns(4)
    a.metric('Risk score',f"{row.hygiene_risk_score:.1f}")
    b.metric('Risk level',str(row.risk_level))
    c.metric('Top driver',row.top_driver)
    d.metric('Current level',f"{row.current_level_pct:.0f}%")
    comp={'Cleaning overdue':min(row.days_since_cleaning/180*100,100),'Bacterial risk':row.bacterial_risk_index,'Turbidity':min(row.turbidity_ntu/10*100,100),'pH deviation':min(abs(row.ph-6.5)/1.5*100,100),'Overflow':min(row.overflow_events_30d/5*100,100),'Maintenance':min(row.maintenance_overdue_days/90*100,100),'Condition':100-row.condition_score}
    cf=pd.DataFrame({'Signal':list(comp),'Pressure':[round(v,1) for v in comp.values()]})
    fig=px.bar(cf,x='Pressure',y='Signal',orientation='h',text_auto='.1f',height=380)
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=0),paper_bgcolor='white',yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig,width='stretch')
    st.dataframe(scored[scored.tank_name==tank].T.reset_index().rename(columns={'index':'field',0:'value'}),use_container_width=True,hide_index=True)

elif page=='Tank Explorer':
    st.markdown("<div class='section-title'>Tank Explorer</div><div class='section-sub'>Filter the monitored network and inspect tank-level operating conditions.</div>",unsafe_allow_html=True)
    f1,f2,f3=st.columns(3)
    zones=f1.multiselect('Zone',sorted(scored.zone.unique()),default=sorted(scored.zone.unique()))
    levels=f2.multiselect('Risk level',['Low','Moderate','High','Critical'],default=['Low','Moderate','High','Critical'])
    minscore=f3.slider('Minimum risk score',0.0,100.0,0.0,1.0)
    view=scored[scored.zone.isin(zones)&scored.risk_level.isin(levels)&(scored.hygiene_risk_score>=minscore)].sort_values('hygiene_risk_score',ascending=False)
    st.dataframe(view[['tank_id','tank_name','zone','tank_type','hygiene_risk_score','risk_level','top_driver','days_since_cleaning','bacterial_risk_index','overflow_events_30d','maintenance_overdue_days','current_level_pct']],use_container_width=True,height=500)

elif page=='Maintenance Planner':
    st.markdown("<div class='section-title'>Maintenance Planner</div><div class='section-sub'>Prioritize cleaning and engineering review using transparent signals.</div>",unsafe_allow_html=True)
    horizon=st.slider('Flag tanks with cleaning age above (days)',30,240,120,10)
    plan=scored[(scored.days_since_cleaning>=horizon)|(scored.maintenance_overdue_days>0)|(scored.risk_level.isin(['High','Critical']))].copy()
    plan['recommended_action']=np.select([plan.risk_level.eq('Critical'),plan.days_since_cleaning>=180,plan.maintenance_overdue_days>0],[ 'Immediate hygiene & inspection review','Schedule full cleaning and hygiene verification','Schedule maintenance review'],'Routine monitoring')
    st.dataframe(plan[['tank_name','zone','risk_level','hygiene_risk_score','days_since_cleaning','maintenance_overdue_days','overflow_events_30d','recommended_action']].sort_values('hygiene_risk_score',ascending=False),use_container_width=True,height=480)
    st.download_button('⬇ Download maintenance priority CSV',plan.to_csv(index=False).encode(),'water_tank_maintenance_priority.csv','text/csv')

elif page=='Historical Trends':
    st.markdown("<div class='section-title'>Historical Hygiene Trends</div><div class='section-sub'>Track storage, usage, turbidity, bacterial risk, and overflow signals over time.</div>",unsafe_allow_html=True)
    ids=scored.tank_id.tolist(); tankid=st.selectbox('Tank', ['All tanks']+ids)
    h=history if tankid=='All tanks' else history[history.tank_id==tankid]
    agg=h.groupby('date',as_index=False).agg(level_pct=('level_pct','mean'),turbidity_ntu=('turbidity_ntu','mean'),bacterial_risk_index=('bacterial_risk_index','mean'),usage_lpd=('usage_lpd','mean'),overflow_events=('overflow_events','sum'))
    c1,c2=st.columns(2)
    with c1:
        fig=px.line(agg,x='date',y='level_pct',markers=True,title='Average storage level (%)',height=320); fig.update_layout(paper_bgcolor='white'); st.plotly_chart(fig,width='stretch')
    with c2:
        fig=px.line(agg,x='date',y='bacterial_risk_index',markers=True,title='Bacterial-risk trend',height=320); fig.update_layout(paper_bgcolor='white'); st.plotly_chart(fig,width='stretch')
    st.dataframe(h,use_container_width=True,height=380)

elif page=='Scenario Simulator':
    st.markdown("<div class='section-title'>Scenario Simulator</div><div class='section-sub'>Explore how cleaning, bacterial-risk, turbidity, overflow, and maintenance improvements could change a screening score.</div>",unsafe_allow_html=True)
    tank=st.selectbox('Base tank',scored['tank_name'].tolist())
    row=scored[scored.tank_name==tank].iloc[0]
    c1,c2=st.columns(2)
    clean_reduction=c1.slider('Days-since-cleaning reduction',0.0,180.0,60.0,5.0)
    bacterial_reduction=c2.slider('Bacterial-risk reduction',0.0,80.0,25.0,5.0)
    turb_reduction=c1.slider('Turbidity reduction',0.0,8.0,2.0,0.5)
    overflow_reduction=c2.slider('Overflow-event reduction',0.0,5.0,1.0,1.0)
    maint_days_reduction=c1.slider('Maintenance-overdue reduction',0.0,90.0,30.0,5.0)
    sim=row.copy()
    sim.days_since_cleaning=max(0,row.days_since_cleaning-clean_reduction); sim.bacterial_risk_index=max(0,row.bacterial_risk_index-bacterial_reduction); sim.turbidity_ntu=max(0,row.turbidity_ntu-turb_reduction); sim.overflow_events_30d=max(0,row.overflow_events_30d-overflow_reduction); sim.maintenance_overdue_days=max(0,row.maintenance_overdue_days-maint_days_reduction)
    sdf=pd.DataFrame([sim.to_dict()]); s=scored.copy(); new=score_tanks(sdf).iloc[0]
    a,b,c=st.columns(3); a.metric('Current',f"{row.hygiene_risk_score:.1f}"); b.metric('Scenario',f"{new.hygiene_risk_score:.1f}"); c.metric('Change',f"{new.hygiene_risk_score-row.hygiene_risk_score:+.1f}")
    fig=go.Figure(go.Bar(x=[row.hygiene_risk_score,new.hygiene_risk_score],y=['Current','Scenario'],orientation='h',text=[row.hygiene_risk_score,new.hygiene_risk_score],textposition='auto'))
    fig.update_layout(height=250,xaxis_range=[0,100],paper_bgcolor='white',margin=dict(l=0,r=0,t=20,b=0)); st.plotly_chart(fig,width='stretch')
    st.info('Scenario outputs are analytical what-if estimates, not guarantees of hygiene or water safety.')

elif page=='Data Upload':
    st.markdown("<div class='section-title'>Data Upload</div><div class='section-sub'>Upload local CSV files. Nothing is sent to external services.</div>",unsafe_allow_html=True)
    up1=st.file_uploader('Upload tank metrics',type=['csv'])
    up2=st.file_uploader('Upload hygiene history',type=['csv'])
    if up1:
        try:
            tankdf=pd.read_csv(up1); st.dataframe(tankdf.head(20),use_container_width=True); st.success('Tank metrics CSV loaded successfully.')
        except Exception as e: st.error(f'Could not read tank metrics CSV: {e}')
    if up2:
        try:
            hdf=pd.read_csv(up2); st.dataframe(hdf.head(20),use_container_width=True); st.success('Hygiene history CSV loaded successfully.')
        except Exception as e: st.error(f'Could not read hygiene history CSV: {e}')
    if up1:
        try:
            newscore=score_tanks(pd.read_csv(up1)); st.session_state['uploaded_scored']=newscore; st.info(f"Validated {len(newscore)} tank records.")
        except Exception as e: st.error(str(e))
    if up2:
        try:
            newhist=history_summary(pd.read_csv(up2)); st.session_state['uploaded_history']=newhist; st.info(f"Validated {len(newhist)} historical records.")
        except Exception as e: st.error(str(e))

elif page=='Reports':
    st.markdown("<div class='section-title'>Reports & Exports</div><div class='section-sub'>Download local analytical outputs for operational review.</div>",unsafe_allow_html=True)
    st.download_button('⬇ Download scored tank report',scored.to_csv(index=False).encode(),'watertankcare_scored_tanks.csv','text/csv')
    high=scored[scored.risk_level.isin(['High','Critical'])].sort_values('hygiene_risk_score',ascending=False)
    st.download_button('⬇ Download priority review queue',high.to_csv(index=False).encode(),'watertankcare_priority_queue.csv','text/csv')
    st.dataframe(high,use_container_width=True,height=420)
    st.info('This project is a screening and planning aid. It does not certify water quality, potability, contamination status, or regulatory compliance.')
