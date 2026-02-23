# Environment Setting
import pandas as pd
from supabase import create_client, Client
import streamlit as st

# Functions | Data Retrieval & Denormalization
def GetSupabaseClient(supaBaseUrl, supabaseKey) -> Client:
    return create_client(supaBaseUrl, supabaseKey)

@st.cache_data(ttl=600)
def SafeTableFetch(supaBaseUrl, supabaseKey, tableName, pageSize = 1000):
    allData = []
    offset  = 0
    supabase = GetSupabaseClient(supaBaseUrl, supabaseKey)

    while True:
        response = supabase.table(tableName).select('*').range(offset, offset + pageSize - 1).execute()
        if not response.data: break
        allData.extend(response.data)
        offset   += pageSize
    
    return pd.DataFrame(allData)

@st.cache_data(ttl=600)
def GetDenormalizedDataframe(supaBaseUrl, supabaseKey):
    supabase: Client = create_client(supaBaseUrl, supabaseKey)
        
    factWeather      = SafeTableFetch(supaBaseUrl, supabaseKey, 'FactWeather')
    dimCity          = SafeTableFetch(supaBaseUrl, supabaseKey, 'DimCity')
    dimCondition     = SafeTableFetch(supaBaseUrl, supabaseKey, 'DimWeatherCondition')
       
    denormalized = factWeather.merge(dimCity, left_on='CTId', right_on='Id', how='left')
    denormalized = denormalized.merge(dimCondition, left_on='WCId', right_on='Id', how='left')       
        
    denormalized = denormalized.drop(columns=['Id_y', 'CreatedAt_x', 'UpdatedAt_x', 'Id', 'CreatedAt_y', 'UpdatedAt_y'])
    denormalized = denormalized.rename(columns={'Name': 'City'})
    denormalized['FullTimestamp'] = pd.to_datetime(denormalized['FullTimestamp'])

    return denormalized