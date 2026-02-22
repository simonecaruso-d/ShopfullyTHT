# Environment Setting
from datetime import datetime
import json
from pathlib import Path

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