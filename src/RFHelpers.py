# Environment Setting
from datetime import datetime, timezone
import requests

import RFApiUsageLog

# Functions | Helpers
def FetchData(endpoint, parameters, usageLogPath):
    RFApiUsageLog.LogApiCall(endpoint, usageLogPath)
    response = requests.get(endpoint, params=parameters)
    if response.status_code == 200: 
        return response.json()
    else:
        print(f'API call failed for {parameters} with status {response.status_code}')
        return None

def ParseHourlyData(hour, cityId, retrievalTime):
    weather = hour.get('weather', [{}])[0]
    
    return {'CTId': cityId,
            'WCId': weather.get('id'),
            'FullTimestamp': datetime.fromtimestamp(hour['dt'], tz=timezone.utc).replace(minute=0, second=0, microsecond=0, tzinfo=None),
            'Temperature': hour.get('temp'),
            'FeltTemperature': hour.get('feels_like'),
            'Humidity': hour.get('humidity'),
            'Clouds': hour.get('clouds'),
            'WindSpeed': hour.get('wind_speed'),
            'RainProbability': hour.get('pop'),
            'RainVolume': hour.get('rain').get('1h') if hour.get('rain') else None,
            'RetrievalTime': retrievalTime.replace(tzinfo=None, microsecond=0),
            'IsCurrent': True}