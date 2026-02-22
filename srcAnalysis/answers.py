# Environment Setting
from dotenv import load_dotenv
import os
import pandas as pd
from supabase import create_client, Client

# Endpoints & Environment Variables
load_dotenv()
SupaBaseUrl         = os.getenv('SUPABASE_URL')
SupabaseKey         = os.getenv('SUPABASE_KEY')

# Functions | Helpers
def SafeTableFetch(supabase, tableName, pageSize = 1000):
    allData = []
    offset  = 0
    
    while True:
        response = supabase.table(tableName).select('*').range(offset, offset + pageSize - 1).execute()
        if not response.data: break
        allData.extend(response.data)
        offset   += pageSize
    
    return pd.DataFrame(allData)

# Functions | Data Retrieval & Denormalization
def GetDenormalizedDataframe(supaBaseUrl, supabaseKey):
    supabase: Client = create_client(supaBaseUrl, supabaseKey)
        
    factWeather      = SafeTableFetch(supabase, 'FactWeather')
    dimCity          = SafeTableFetch(supabase, 'DimCity')
    dimCondition     = SafeTableFetch(supabase, 'DimWeatherCondition')
       
    denormalized = factWeather.merge(dimCity, left_on='CTId', right_on='Id', how='left')
    denormalized = denormalized.merge(dimCondition, left_on='WCId', right_on='Id', how='left')       
        
    denormalized = denormalized.drop(columns=['Id_y', 'CreatedAt_x', 'UpdatedAt_x', 'Id', 'CreatedAt_y', 'UpdatedAt_y'])
    denormalized = denormalized.rename(columns={'Name': 'City'})
    denormalized['FullTimestamp'] = pd.to_datetime(denormalized['FullTimestamp'])

    return denormalized

# Functions | Answer Questions
def DistinctWeatherConditions(df, periodEnd='2026-02-19 04:00:00'):
    filtered = df[(df['DataType'] == 'Actual') & (df['FullTimestamp'] <= periodEnd) & (df['IsCurrent'] == True)]
    count    = filtered['WCId'].nunique()
    
    return count

def MostCommonWeatherConditionsPerCity(df, periodStart='2026-02-24 11:00:00'):
    filtered = df[(df['DataType'] == 'Forecast') & (df['FullTimestamp'] >= periodStart) & (df['IsCurrent'] == True)]
    result   = filtered.groupby(['City', 'MainCondition']).size().reset_index(name='Count')
    result   = result.sort_values(['City', 'Count'], ascending=[True, False])
    
    return result[['City', 'MainCondition', 'Count']].to_dict('records')

def AverageTemperaturePerCity(df, periodEnd='2026-02-19 04:00:00'):
    filtered       = df[(df['DataType'] == 'Actual') & (df['FullTimestamp'] <= periodEnd) & (df['IsCurrent'] == True)]
    result         = filtered.groupby('City')['Temperature'].mean().round(2).reset_index()
    result.columns = ['City', 'AverageTemperature']
    result         = result.sort_values('AverageTemperature', ascending=True)
    
    return result.to_dict('records')

def HighestAbsoluteTemperature(df, periodEnd='2026-02-19 04:00:00'):
    filtered       = df[(df['DataType'] == 'Actual') & (df['FullTimestamp'] <= periodEnd) & (df['IsCurrent'] == True)]
    maxTemperature = filtered['Temperature'].max()
    result         = filtered[filtered['Temperature'] == maxTemperature]['City'].unique()
    
    return result.tolist() if len(result) > 0 else None

def HighestDailyTemperatureVariation(df, periodEnd='2026-02-19 04:00:00'):
    filtered         = df[(df['DataType'] == 'Actual') & (df['FullTimestamp'] <= periodEnd) & (df['IsCurrent'] == True)].copy()
    filtered['Date'] = pd.to_datetime(filtered['FullTimestamp']).dt.date
    
    dailyVariations = filtered.groupby(['Date', 'City'])['Temperature'].apply(lambda x: x.max() - x.min()).reset_index(name='variation')
    result          = dailyVariations.loc[dailyVariations.groupby('Date')['variation'].idxmax()][['Date', 'City']]
    
    return result.to_dict('records')

def StrongestWind(df, periodEnd='2026-02-19 04:00:00'):
    filtered = df[(df['DataType'] == 'Actual') & (df['FullTimestamp'] <= periodEnd) & (df['IsCurrent'] == True)]
    maxWind  = filtered['WindSpeed'].max()
    result   = filtered[filtered['WindSpeed'] == maxWind]['City'].unique()
    
    return result.tolist()

# Functions | Print Results
def PrintResults(resultsDictionary):
    for question, answer in resultsDictionary.items():
        print(f'Question: {question}')
        print('Answer:')
        if isinstance(answer, list):
            for item in answer: print(f'  - {item}')
        elif isinstance(answer, dict):
            for key, value in answer.items(): print(f'  {key}: {value}')
        else: print(f'  {answer}')

# Run 
DenormalizedDf = GetDenormalizedDataframe(SupaBaseUrl, SupabaseKey)

ResultsDictionary = {
    'DistinctWeatherConditions'         : DistinctWeatherConditions(DenormalizedDf),
    'MostCommonWeatherConditionsPerCity': MostCommonWeatherConditionsPerCity(DenormalizedDf),
    'AverageTemperaturePerCity'         : AverageTemperaturePerCity(DenormalizedDf),
    'HighestAbsoluteTemperature'        : HighestAbsoluteTemperature(DenormalizedDf),
    'HighestDailyTemperatureVariation'  : HighestDailyTemperatureVariation(DenormalizedDf),
    'StrongestWind'                     : StrongestWind(DenormalizedDf)}

PrintResults(ResultsDictionary)