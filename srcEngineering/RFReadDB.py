# Environment Setting
from supabase import create_client, Client
import pandas as pd

# Functions | Supabase Retrieval
def GetCityTable(supaBaseUrl, supabaseKey):
    try:
        supabase: Client = create_client(supaBaseUrl, supabaseKey)
        response = supabase.table('DimCity').select('"Id", "Latitude", "Longitude"').execute()        
        df = pd.DataFrame(response.data)
        return df
    
    except Exception as e:
        print(f'Error connecting to Supabase: {e}')
        return None