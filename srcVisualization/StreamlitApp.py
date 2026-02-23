# Environment Setting
from dotenv import load_dotenv
import os
import streamlit as st

import SAStyling
import SAData
import SAMetrics

# Image URLs
FlippLogoUrl     = 'https://cdn.brandfetch.io/idjav1wjnv/w/1000/h/1000/theme/dark/icon.png?c=1dxbfHSJFAPEGdCLU4o5B'
ShopfullyLogoUrl = 'https://shopfully.com/wp-content/uploads/2025/02/Shopfully_Avatar_RGB_Purple_Background.png'

# Environment Variables
load_dotenv()
SupaBaseUrl = st.secrets['SUPABASE_URL']
SupabaseKey = st.secrets['SUPABASE_KEY']

# App
SAStyling.TopBar(FlippLogoUrl, ShopfullyLogoUrl)

DenormalizedDf = SAData.GetDenormalizedDataframe(SupaBaseUrl, SupabaseKey)
CurrentDf = DenormalizedDf[DenormalizedDf['IsCurrent'] == True]

Tab1, Tab2 = SAStyling.PageNavigatorTabs()
with Tab1: 
    FiltersExplore = SAStyling.RenderFilters('Explore Weather', DenormalizedDf)
    FilteredDf = SAMetrics.FilterDf(CurrentDf, FiltersExplore['City'], FiltersExplore['DataType'], FiltersExplore['FullTimestamp'])

    st.markdown('<br><br>', unsafe_allow_html=True)
    metrics = SAMetrics.ComputeWeatherMetrics(FilteredDf)
    SAStyling.RenderMetrics(metrics)

    st.markdown('<br><br>', unsafe_allow_html=True)
    PrintDf = FilteredDf.rename(columns={'FullTimestamp': 'Timestamp', 'DataType': 'Data Type', 'FeltTemperature': 'Felt Temperature', 'WindSpeed': 'Wind Speed', 'MainCondition': 'Forecast', 'DetailedCondition': 'Detail'})
    PrintDf = PrintDf[['Country', 'Region', 'Province', 'City', 'Timestamp', 'Data Type', 'Temperature', 'Felt Temperature', 'Humidity', 'Clouds', 'Wind Speed', 'Forecast', 'Detail']]
    SAStyling.RenderTable(PrintDf, title="🌤️ Weather Data Explorer")
with Tab2: 
    FiltersAccuracy     = SAStyling.RenderFilters('Forecast Accuracy', DenormalizedDf)
    
    st.markdown('<br><br>', unsafe_allow_html=True)
    AccuracyDf      = SAMetrics.FilterDf(DenormalizedDf, FiltersAccuracy['City'], None, FiltersAccuracy['FullTimestamp'])
    Mae, Mape       = SAMetrics.ComputeForecastAccuracy(AccuracyDf, FiltersAccuracy['Parameter'])
    SAStyling.RenderAccuracy(Mae, Mape, FiltersAccuracy['Parameter'])

    st.markdown('<br><br>', unsafe_allow_html=True)
    timeSeriesDf = SAMetrics.PrepareTimeSeriesComparisons(CurrentDf, FiltersAccuracy['Parameter'], FiltersAccuracy['City'])
    SAStyling.RenderForecastChart(timeSeriesDf, FiltersAccuracy['Parameter'])