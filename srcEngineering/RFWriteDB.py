# Environment Setting
import logging
import numpy as np
from supabase import create_client, Client
from tqdm import tqdm

# Logging Configuration
logger = logging.getLogger(__name__)

# Functions | Supabase Writing
def WriteFactWeatherToDatabase(factWeatherDf, supabaseUrl, supabaseKey):
    try:
        supabase: Client   = create_client(supabaseUrl, supabaseKey)
        uniqueCombinations = factWeatherDf[['DataType', 'CTId', 'FullTimestamp']].drop_duplicates()
        
        for _, combination in tqdm(uniqueCombinations.iterrows(), total=len(uniqueCombinations), desc='Marking existing rows as not current'):
            supabase.table('FactWeather').update({'IsCurrent': False}).eq('DataType', combination['DataType']).eq('CTId', int(combination['CTId'])).eq('FullTimestamp', combination['FullTimestamp'].isoformat()).execute()
        
        dataToInsert                  = factWeatherDf.copy()
        dataToInsert['FullTimestamp'] = dataToInsert['FullTimestamp'].astype(str)
        dataToInsert['RetrievalTime'] = dataToInsert['RetrievalTime'].astype(str)
        dataToInsert                  = dataToInsert.where(~dataToInsert.isna(), None)
        dataToInsert                  = dataToInsert.replace([np.inf, -np.inf], None)

        records   = dataToInsert.to_dict('records')
                
        batchSize = 500
        for i in tqdm(range(0, len(records), batchSize), desc='Inserting new rows'):
            batch    = records[i:i + batchSize]
            response = supabase.table('FactWeather').insert(batch).execute()
        
    except Exception as e:
        logger.error(f'Error writing to Supabase: {e}', exc_info=True)
        raise

    return