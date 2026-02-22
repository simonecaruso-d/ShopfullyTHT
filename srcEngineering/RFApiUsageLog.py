# Environment Setting
from datetime import datetime
import json
from pathlib import Path
import logging
from supabase import create_client, Client

import RetrieveFacts

# Logging Configuration
logger = logging.getLogger(__name__)

# Functions | API Usage Tracking
def LogApiCall(endpoint, usageLogPath):
    today = datetime.now().strftime("%Y-%m-%d")
    log = {}

    path = Path(usageLogPath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists(): path.write_text('timestamp,endpoint\n', encoding='utf-8')

    with path.open('a', encoding='utf-8') as file:
        for line in file:
            try:
                entry = json.loads(line)
                key = entry['Date']
                log[key] = entry
            except: continue

    if today not in log: log[today] = {'Date': today, 'TotalCalls': 0, 'Endpoints': {}}

    log[today]['TotalCalls'] += 1

    ep = endpoint.split('/')[-1]
    if ep not in log[today]['Endpoints']: log[today]['Endpoints'][ep] = 0
    log[today]['Endpoints'][ep] += 1

    with open(usageLogPath, 'w', encoding='utf-8') as file:
        for entry in log.values(): 
            file.write(json.dumps(entry) + '\n')

    return

def LogApiCallToSupabase(endpoint, supabaseUrl=RetrieveFacts.SupaBaseUrl, supabaseKey=RetrieveFacts.SupaKey, tableName='ApiUsageLog'):
    try:
        supabase: Client = create_client(supabaseUrl, supabaseKey)
        today = datetime.now().strftime("%Y-%m-%d")
        endpointCorrect = endpoint.split('/')[-1]
        
        todayRecord = supabase.table(tableName).select('*').eq('Date', today).execute()
        
        if todayRecord.data:
            existingRecord = todayRecord.data[0]
            totalCalls = existingRecord.get('TotalCalls', 0) + 1
            endpoints = existingRecord.get('Endpoints', {}) if isinstance(existingRecord.get('Endpoints'), dict) else {}
            
            if endpointCorrect not in endpoints: endpoints[endpointCorrect] = 0
            endpoints[endpointCorrect] += 1
            
            supabase.table(tableName).update({'TotalCalls': totalCalls, 'Endpoints': endpoints}).eq('Date', today).execute()
        else:
            newRecord = {'Date': today, 'TotalCalls': 1, 'Endpoints': {endpointCorrect: 1}}
            supabase.table(tableName).insert(newRecord).execute()
            
    except Exception as e:
        logger.error(f'Error logging API call to Supabase: {e}', exc_info=True)
        raise

    return