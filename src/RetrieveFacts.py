# Environment Setting
from dotenv import load_dotenv
import os
from pathlib import Path

import RFCallAPI
import RFReadDB
import RFWriteDB

# Environment Variables
load_dotenv()
OpenWeatherApiKEY = os.getenv('OPENWEATHER_API_KEY')
SupaBaseUrl = os.getenv('SUPABASE_URL')
SupabaseKey = os.getenv('SUPABASE_KEY')

# File Paths
BaseDirectory = Path(__file__).resolve().parent
UsageLogPath = BaseDirectory.parent / 'log' / 'ApiUsageLog.txt'

# Endpoints
BaseEndpoint = 'https://api.openweathermap.org/data/3.0/onecall'

# Run
Cities = RFReadDB.GetCityTable(SupaBaseUrl, SupabaseKey)
FactWeather = RFCallAPI.GetForecastsAndActuals(Cities, OpenWeatherApiKEY, BaseEndpoint, UsageLogPath)
RFWriteDB.WriteFactWeatherToDatabase(FactWeather, SupaBaseUrl, SupabaseKey)