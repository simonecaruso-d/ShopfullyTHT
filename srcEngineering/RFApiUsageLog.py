# Environment Setting
from datetime import datetime
import logging
import time
from collections import defaultdict
from supabase import create_client, Client
from postgrest.exceptions import APIError

# Logging Configuration
logger             = logging.getLogger(__name__)

ApiCallAccumulator = defaultdict(lambda: defaultdict(int))

# Static Inputs
MaxRetries   = 3
InitialDelay = 2

# Functions | Old (Immediate Write)
def LogApiCallToSupabasePre(endpoint, supabaseUrl, supabaseKey, tableName='ApiUsageLog'):
    try:
        supabase: Client = create_client(supabaseUrl, supabaseKey)
        now              = datetime.now()
        today            = now.strftime("%Y-%m-%d")
        updatedAt        = now.isoformat()
        endpointCorrect  = endpoint.split('/')[-1]
        
        todayRecord      = supabase.table(tableName).select('*').eq('Date', today).execute()
        
        if todayRecord.data:
            existingRecord = todayRecord.data[0]
            totalCalls     = existingRecord.get('TotalCalls', 0) + 1
            endpoints      = existingRecord.get('Endpoints', {}) if isinstance(existingRecord.get('Endpoints'), dict) else {}
            
            if endpointCorrect not in endpoints: endpoints[endpointCorrect] = 0
            endpoints[endpointCorrect]                                      += 1
            
            supabase.table(tableName).update({'TotalCalls': totalCalls, 'Endpoints': endpoints, 'UpdatedAt': updatedAt}).eq('Date', today).execute()
        else:
            newRecord = {'Date': today, 'TotalCalls': 1, 'Endpoints': {endpointCorrect: 1}, 'UpdatedAt': updatedAt}
            supabase.table(tableName).insert(newRecord).execute()
            
    except Exception as e:
        logger.error(f'Error logging API call to Supabase: {e}', exc_info=True)
        raise

    return

# Functions | New (Batch Accumulation + Flush)
def AccumulateApiCall(endpoint, apiCallAccumulator = ApiCallAccumulator):
    endpointCorrect                            = endpoint.split('/')[-1]
    today                                      = datetime.now().strftime("%Y-%m-%d")
    apiCallAccumulator[today][endpointCorrect] += 1
    logger.debug(f'API call accumulated: {endpointCorrect}')
    return

def FlushApiCallBatch(supabaseUrl, supabaseKey, apiCallAccumulator = ApiCallAccumulator, tableName='ApiUsageLog', maxRetries=MaxRetries, initialDelay=InitialDelay):
    if not apiCallAccumulator:
        logger.info('No accumulated API calls to flush.')
        return True
    
    supabase: Client = create_client(supabaseUrl, supabaseKey)
    updatedAt = datetime.now().isoformat()
    
    for attempt in range(maxRetries):
        try:
            for dateKey, endpointsDictionary in apiCallAccumulator.items():
                totalCalls  = sum(endpointsDictionary.values())
                
                todayRecord = supabase.table(tableName).select('*').eq('Date', dateKey).execute()
                
                if todayRecord.data:
                    existingRecord    = todayRecord.data[0]
                    existingEndpoints = existingRecord.get('Endpoints', {}) if isinstance(existingRecord.get('Endpoints'), dict) else {}
                    
                    for endpoint, count in endpointsDictionary.items(): existingEndpoints[endpoint] = existingEndpoints.get(endpoint, 0) + count
                    
                    newTotalCalls = existingRecord.get('TotalCalls', 0) + totalCalls
                    supabase.table(tableName).update({'TotalCalls': newTotalCalls, 'Endpoints': existingEndpoints, 'UpdatedAt': updatedAt}).eq('Date', dateKey).execute()
                    
                    logger.info(f'Updated {dateKey}: +{totalCalls} calls, Total: {newTotalCalls}')
                else:
                    newRecord = {'Date': dateKey, 'TotalCalls': totalCalls, 'Endpoints': dict(endpointsDictionary), 'UpdatedAt': updatedAt}
                    supabase.table(tableName).insert(newRecord).execute()
                    logger.info(f'Created new record for {dateKey}: {totalCalls} calls')
            
            apiCallAccumulator.clear()
            logger.info('API call batch flushed successfully.')
            return True
            
        except APIError as e:
            errorCode = e.args[0].get('code') if e.args and isinstance(e.args[0], dict) else None
            
            if errorCode in (502, 503) and attempt < maxRetries - 1:
                delay = initialDelay * (2 ** attempt)
                logger.warning(f'Supabase error {errorCode} on attempt {attempt + 1}/{maxRetries}. Retrying in {delay}s...')
                time.sleep(delay)
            else:
                logger.error(f'Error flushing API call batch (attempt {attempt + 1}/{maxRetries}): {e}', exc_info=True)
                return False
                
        except Exception as e:
            logger.error(f'Unexpected error flushing API call batch: {e}', exc_info=True)
            return False
    
    return False