# Environment Setting
from datetime import datetime, timezone
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import RFApiUsageLog

# Logging Configuration
logger = logging.getLogger(__name__)

# Functions | Helpers
def FetchData(endpoint, parameters, usageLogPath):
    RFApiUsageLog.LogApiCall(endpoint, usageLogPath)
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    try:
        response = session.get(endpoint, params=parameters, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'API call failed for {parameters}', exc_info=True)
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