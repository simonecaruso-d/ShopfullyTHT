# Environment Setting
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Functions | Helpers
def GetLastUpdateSlot():
    utcNow = datetime.now(pytz.utc)
    hour = utcNow.hour
    slots = [5, 11, 16, 20]
    pastSlots = [s for s in slots if s <= hour]
    lastHour = max(pastSlots) if pastSlots else 20
    lastUpdate = utcNow.replace(hour=lastHour, minute=0, second=0, microsecond=0)
    
    return lastUpdate.strftime("%H:%M")

# Functions | Top Bar & Custom Styling
def TopBar(flippLogoUrl, shopfullyLogoUrl):
    st.set_page_config(page_title='Shopfully Weather THT', page_icon='🌤️', layout='wide')
 
    lastUpdateTime = GetLastUpdateSlot()
    
    st.markdown("""<style>
                /* Page background */
                [data-testid="stAppViewContainer"] {background-color: #121212;}

                /* Topbar container */
                .topbar {position: sticky; top: 0; display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; border-radius: 18px; margin-bottom: 25px; background: rgba(118, 15, 202, 1); box-shadow: 0 0 12px rgba(67,196,244,0.6), 0 4px 24px rgba(0,0,0,0.3); z-index: 999; transition: box-shadow 0.3s ease;}

                /* Left section */
                .left-section {display: flex; align-items: center; gap: 14px;}

                /* Logos */
                .logo {height: 36px; border-radius: 8px; transition: transform 0.3s ease, box-shadow 0.3s ease;}
                .logo:hover {transform: scale(1.15); box-shadow: 0 0 14px rgba(67,196,244,0.8);}

                /* Title */
                .title {font-size: 22px; font-weight: 600; margin-left: 12px; color: #ffffff; transition: text-shadow 0.3s ease;}
                .title:hover {text-shadow: 0 0 14px rgba(67,196,244,0.8);}

                /* Right section */
                .right-section {text-align: right; font-size: 14px; color: #ffffff;}

                /* Status */
                .status {display: flex; align-items: center; justify-content: flex-end; gap: 8px; margin-top: 6px;}

                /* Pulse dot */
                .green-dot {width: 14px; height: 14px; background-color: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e; animation: pulse 1.5s infinite;}

                @keyframes pulse {
                    0% { transform: scale(0.8); opacity: 0.7; }
                    50% { transform: scale(1.3); opacity: 1; } 
                    100% { transform: scale(0.8); opacity: 0.7; }}
                </style>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="topbar">
        <div class="left-section">
            <img src="{flippLogoUrl}" class="logo"><img src="{shopfullyLogoUrl}" class="logo"><div class="title">Shopfully Weather Take Home Test</div>
        </div>
        <div class="right-section">
            <div><strong>Author:</strong> Simone Caruso</div>
            <div class="status"><div class="green-dot"></div><div>Data Updated at {lastUpdateTime} (UTC)</div>
            </div></div></div>""", unsafe_allow_html=True)
    
    return 

# Functions | Page Selector
def PageNavigatorTabs():
    st.markdown("""<style>
    div[role="tablist"] {display: flex; justify-content: stretch; margin: 20px 32px 10px 32px; gap: 0px;}
    button[data-baseweb="tab"] {flex: 1; background-color: rgba(118,15,202,0.15) !important; color: #ffffff !important; font-weight: 600 !important; font-size: 14px !important; border-radius: 14px !important; padding: 8px 0px !important; transition: background-color 0.3s ease, box-shadow 0.3s ease; border-bottom: 0px solid transparent !important;}
    button[data-baseweb="tab"]:hover {background-color: rgba(118,15,202,0.4) !important; box-shadow: 0 4px 12px rgba(67,196,244,0.4) !important;}
    button[data-baseweb="tab"][aria-selected="true"] {background-color: rgba(118,15,202,1) !important; box-shadow: 0 4px 16px rgba(67,196,244,0.6) !important; border-bottom: 0px solid transparent !important;}
    </style>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:16px; font-weight:700; color:rgba(118,15,202,0.9); letter-spacing:0.5px; margin-bottom:6px;">Navigation</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(['Explore Weather', 'Forecast Accuracy'])

    return tab1, tab2

# Functions | Filters
def RenderFilters(tabName, df, parameterOptions=['Temperature', 'FeltTemperature', 'Humidity', 'Clouds', 'WindSpeed']):
    st.markdown('<div style="font-size:16px; font-weight:700; color:rgba(67,196,244,0.9); letter-spacing:0.5px; margin-bottom:6px;">Filters</div>', unsafe_allow_html=True)

    st.markdown("""<style>
    [data-testid="stHorizontalBlock"] {background-color: rgba(67, 196, 244, 0.1); border-radius: 14px; padding: 12px 16px; margin-bottom: 20px; gap: 12px; align-items: flex-end;}
    [data-testid="stHorizontalBlock"] label {color: #ffffff !important; font-weight: 600 !important; font-size: 13px !important;}
    [data-testid="stHorizontalBlock"] .stMultiSelect [data-baseweb="select"] > div,
    [data-testid="stHorizontalBlock"] .stSelectbox [data-baseweb="select"] > div {background-color: rgba(67, 196, 244, 0.2) !important; border-radius: 20px !important; border: none !important; color: #ffffff !important; transition: background-color 0.2s ease;}
    [data-testid="stHorizontalBlock"] .stMultiSelect [data-baseweb="select"] > div:focus-within,
    [data-testid="stHorizontalBlock"] .stSelectbox [data-baseweb="select"] > div:focus-within {background-color: rgba(67, 196, 244, 0.35) !important; box-shadow: 0 0 8px rgba(67, 196, 244, 0.6) !important;}
    [data-testid="stHorizontalBlock"] [data-baseweb="tag"] {background-color: rgba(67, 196, 244, 0.4) !important; border-radius: 12px !important; color: #ffffff !important;}
    [data-testid="stHorizontalBlock"] .stDateInput input {background-color: rgba(67, 196, 244, 0.2) !important; border-radius: 20px !important; border: none !important; color: #ffffff !important; padding: 6px 12px; transition: background-color 0.2s ease;}
    [data-testid="stHorizontalBlock"] .stDateInput input:focus {background-color: rgba(67, 196, 244, 0.35) !important; box-shadow: 0 0 8px rgba(67, 196, 244, 0.6) !important;}
    [data-testid="stHorizontalBlock"] [data-baseweb="select"] span,
    [data-testid="stHorizontalBlock"] [data-baseweb="select"] div {color: #ffffff !important;}
    </style>""", unsafe_allow_html=True)

    selectedFilters = {}

    columnCity, columnDate, columnSpecific = st.columns([1.5, 2, 1.5])

    with columnCity:
        cities = df['City'].dropna().unique().tolist()
        selectedCity = st.multiselect('City', options=cities, default=[cities[0]], key=f'{tabName}_city')
        selectedFilters['City'] = selectedCity

    with columnDate:
        minDate = pd.to_datetime(df['FullTimestamp']).min()
        maxDate = pd.to_datetime(df['FullTimestamp']).max()
        selectedDates = st.date_input('Date Range', value=[minDate, maxDate], key=f'{tabName}_daterange')
        if len(selectedDates) == 2: selectedFilters['FullTimestamp'] = selectedDates
        else: st.stop()

    with columnSpecific:
        if tabName == 'Explore Weather':
            dataTypes = df['DataType'].dropna().unique().tolist()
            selectedDataType = st.selectbox('Data Type', options=dataTypes, key=f'{tabName}_datatype')
            selectedFilters['DataType'] = selectedDataType

        elif tabName == 'Forecast Accuracy':
            selectedParameter = st.selectbox('Parameter', options=parameterOptions, key=f'{tabName}_parameter')
            selectedFilters['Parameter'] = selectedParameter

    return selectedFilters

# Functions | Metrics
def RenderMetrics(metrics):
    units     = {'Temperature': '°C', 'Felt Temperature': '°C', 'Humidity': '%', 'Clouds': '%', 'Wind Speed': 'm/s'}
    rowColors = {'Temperature': '255, 235, 100', 'Felt Temperature': '210, 235, 90', 'Humidity': '160, 230, 110', 'Clouds': '120, 225, 130', 'Wind Speed': '100, 220, 160'}
    colsOrder = ['Minimum', 'Average', 'Maximum', 'Standard Deviation']

    st.markdown("""
    <style>
    .metrics-grid {display: grid; grid-template-columns: 160px repeat(4, 1fr); gap: 8px; margin-bottom: 8px;}
    .metric-col-header {border-radius: 10px; padding: 10px 14px; text-align: center; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;}
    .metric-box {border-radius: 10px; padding: 10px 14px; text-align: center; transition: all 0.2s ease; cursor: default;}
    .metric-box:hover {filter: brightness(1.3);}
    .metric-value {font-size: 17px; font-weight: 700; letter-spacing: 0.5px;}
    </style>
    <div style="font-size:16px; font-weight:700; color:#e0e0e0; margin-bottom:8px; letter-spacing:0.5px;">📊 Weather Metrics</div>
    """, unsafe_allow_html=True)

    headerHtml  = '<div class="metrics-grid"><div style="background:transparent;border:none;"></div>'
    headerHtml += ''.join(f'<div class="metric-col-header" style="background-color:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08); color:#e0e0e0;">{col}</div>' for col in colsOrder)
    headerHtml += '</div>'
    st.markdown(headerHtml, unsafe_allow_html=True)

    for rowLabel, rowData in metrics.items():
        unit = units.get(rowLabel, '')
        rgb  = rowColors.get(rowLabel, '255,255,255')

        rowHtml  = f'<div class="metrics-grid"><div class="metric-col-header" style="background-color:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08); color:#e0e0e0;">{rowLabel}</div>'
        rowHtml += ''.join(f'<div class="metric-box" style="background-color:rgba({rgb},0.07); border:1px solid rgba({rgb},0.2);"><div class="metric-value" style="color:rgba({rgb},1); text-shadow:0 0 8px rgba({rgb},0.5);">{rowData.get(col)} <span style="font-size:12px; opacity:0.6;">{unit}</span></div></div>' for col in colsOrder)
        rowHtml += '</div>'
        st.markdown(rowHtml, unsafe_allow_html=True)

# Functions | Dataframe
def RenderTable(df, title=None, height=300):
    header = ''.join(f'<th>{col}</th>' for col in df.columns)
    rows = ''.join('<tr>' + ''.join(f'<td>{val}</td>' for val in row) + '</tr>' for row in df.itertuples(index=False))
    titleHtml = f'<div class="section-title">{title}</div>' if title else ''

    st.markdown(f"""<style>
        .section-title {{font-size: 16px; font-weight: 700; color: #e0e0e0; margin-bottom: 8px; letter-spacing: 0.5px;}}
        .table-wrapper {{overflow-x: auto; overflow-y: auto; max-height: {height}px; border-radius: 14px; box-shadow: 0 0 12px rgba(255,255,255,0.15), 0 0 30px rgba(255,255,255,0.05); margin-bottom: 20px; scrollbar-width: thin; scrollbar-color: rgba(255,255,255,0.3) transparent;}}
        .table-wrapper::-webkit-scrollbar {{width: 6px; height: 6px;}}
        .table-wrapper::-webkit-scrollbar-track {{background: transparent;}}
        .table-wrapper::-webkit-scrollbar-thumb {{background-color: rgba(255,255,255,0.25); border-radius: 10px;}}
        .styled-table {{width: 100%; border-collapse: collapse; font-size: 13px; font-family: inherit;}}
        .styled-table thead tr {{position: sticky; top: 0; z-index: 1;}}
        .styled-table th {{background-color: rgba(255,255,255,0.1); color: #ffffff; font-weight: 700; padding: 10px 14px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.3); white-space: nowrap; text-shadow: 0 0 6px rgba(255,255,255,0.6); letter-spacing: 1px;}}
        .styled-table td {{background-color: rgba(255,255,255,0.02); color: #c0c0c0; padding: 8px 14px; border-bottom: 1px solid rgba(255,255,255,0.06); white-space: nowrap;}}
        .styled-table tr:hover td {{background-color: rgba(255,255,255,0.07); color: #ffffff; text-shadow: 0 0 6px rgba(255,255,255,0.4); transition: all 0.2s ease;}}
        .styled-table tr:last-child td {{border-bottom: none;}}
        </style>""", unsafe_allow_html=True)

    st.markdown(f'{titleHtml}<div class="table-wrapper"><table class="styled-table"><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

# Functions | Accuracy Metrics
def RenderAccuracy(mae, mape, parameter):
    units = {'Temperature': '°C', 'FeltTemperature': '°C', 'Humidity': '%', 'Clouds': '%', 'WindSpeed': 'm/s'}
    unit  = units.get(parameter, '')

    if   mape < 25:  mapeColor = '100, 220, 160'
    elif mape < 75:  mapeColor = '255, 235, 100'
    else:            mapeColor = '220, 80, 100'

    st.markdown("""<style>
    .accuracy-grid {display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 8px;}
    .accuracy-box {border-radius: 10px; padding: 16px 20px; text-align: center; transition: all 0.2s ease; cursor: default;}
    .accuracy-box:hover {filter: brightness(1.3);}
    .accuracy-label {font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #e0e0e0; margin-bottom: 8px;}
    .accuracy-value {font-size: 28px; font-weight: 700; text-shadow: 0 0 8px rgba(255,255,255,0.5), 0 0 20px rgba(255,255,255,0.2);}
    .accuracy-unit {font-size: 14px; opacity: 0.5; margin-left: 4px;}
    </style>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-size:16px; font-weight:700; color:#e0e0e0; margin-bottom:8px; letter-spacing:0.5px;">🎯 Forecast Accuracy - {parameter}</div>
    <div class="accuracy-grid">
        <div class="accuracy-box" style="background-color:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);">
            <div class="accuracy-label">MAE</div>
            <div class="accuracy-value" style="color:#ffffff;">{mae}<span class="accuracy-unit">{unit}</span></div>
        </div>
        <div class="accuracy-box" style="background-color:rgba({mapeColor},0.07); border:1px solid rgba({mapeColor},0.2);">
            <div class="accuracy-label">MAPE</div>
            <div class="accuracy-value" style="color:rgba({mapeColor},1); text-shadow:0 0 8px rgba({mapeColor},0.5);">{mape}<span class="accuracy-unit">%</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

# Functions | Line Chart
def RenderForecastChart(df, parameter):
    colors = {'Actual': 'rgba(67, 196, 244, 1)', 'Forecast': 'rgba(118, 15, 202, 1)'}
    glows  = {'Actual': 'rgba(67, 196, 244, 0.3)', 'Forecast': 'rgba(118, 15, 202, 0.3)'}

    fig = go.Figure()

    for col, color in colors.items():
        if col in df.columns:
            fig.add_trace(go.Scatter(x=df['FullTimestamp'], y=df[col], mode='lines', name=col, line=dict(color=color, width=2), fillcolor=glows[col]))
            fig.add_trace(go.Scatter(x=df['FullTimestamp'], y=df[col], mode='lines', name=col, line=dict(color=glows[col], width=8), showlegend=False, hoverinfo='skip'))

    fig.update_layout(
        plot_bgcolor='rgba(35, 35, 35, 0.95)',
        font=dict(color='#e0e0e0'),
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(text=f'📈 Forecast vs Actual - {parameter}', font=dict(size=16, color='#e0e0e0'), y=0.98, x=0, xanchor='left'),
        legend=dict(orientation='h', x=-0.005, xanchor='left', y=1.1, yanchor='top', font=dict(size=10)),        
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)'),)

    st.plotly_chart(fig, use_container_width=True, key='forecast_chart')

# Functions | LLM
def RenderLLMComment(comment: str):
    st.markdown("""<style>
    .llm-box {border-radius: 14px; padding: 18px 24px; margin-top: 8px; margin-bottom: 8px; background-color: rgba(118, 15, 202, 0.07); border: 1px solid rgba(118, 15, 202, 0.35); box-shadow: 0 0 12px rgba(118, 15, 202, 0.2), 0 0 30px rgba(118, 15, 202, 0.05); transition: all 0.2s ease;}
    .llm-box:hover {filter: brightness(1.2);}
    .llm-header {font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(118, 15, 202, 0.9); margin-bottom: 10px;}
    .llm-text {font-size: 14px; color: #c0c0c0; line-height: 1.6;}
    </style>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="llm-box">
        <div class="llm-header">🤖 AI Insight</div>
        <div class="llm-text">{comment}</div>
    </div>""", unsafe_allow_html=True)