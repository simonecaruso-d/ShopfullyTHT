# Environment Setting
from datetime import datetime
import logging
from supabase import create_client, Client

# Logging Configuration
logger = logging.getLogger(__name__)

# Functions | API Usage Tracking
def LogApiCallToSupabase(endpoint, supabaseUrl, supabaseKey, tableName='ApiUsageLog'):
    try:
        supabase: Client = create_client(supabaseUrl, supabaseKey)
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        updatedAt = now.isoformat()
        endpointCorrect = endpoint.split('/')[-1]
        
        todayRecord = supabase.table(tableName).select('*').eq('Date', today).execute()
        
        if todayRecord.data:
            existingRecord = todayRecord.data[0]
            totalCalls = existingRecord.get('TotalCalls', 0) + 1
            endpoints = existingRecord.get('Endpoints', {}) if isinstance(existingRecord.get('Endpoints'), dict) else {}
            
            if endpointCorrect not in endpoints: endpoints[endpointCorrect] = 0
            endpoints[endpointCorrect] += 1
            
            supabase.table(tableName).update({'TotalCalls': totalCalls, 'Endpoints': endpoints, 'UpdatedAt': updatedAt}).eq('Date', today).execute()
        else:
            newRecord = {'Date': today, 'TotalCalls': 1, 'Endpoints': {endpointCorrect: 1}, 'UpdatedAt': updatedAt}
            supabase.table(tableName).insert(newRecord).execute()
            
    except Exception as e:
        logger.error(f'Error logging API call to Supabase: {e}', exc_info=True)
        raise

    return