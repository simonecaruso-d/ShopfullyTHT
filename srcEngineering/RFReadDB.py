# Environment Setting
import logging
import pandas as pd
from supabase import create_client, Client

import RetrieveFacts

# Logging Configuration
logger = logging.getLogger(__name__)

# Functions | Supabase Retrieval
def GetCityTable(supaBaseUrl=None, supabaseKey=None):
    if supaBaseUrl is None: supaBaseUrl = RetrieveFacts.SupaBaseUrl
    if supabaseKey is None: supabaseKey = RetrieveFacts.SupabaseKey
    try:
        supabase: Client = create_client(supaBaseUrl, supabaseKey)
        response = supabase.table('DimCity').select('"Id", "Latitude", "Longitude"').execute()        
        df = pd.DataFrame(response.data)
        return df
    
    except Exception as e:
        logger.error(f'Error retrieving city table: {e}', exc_info=True)
        return None