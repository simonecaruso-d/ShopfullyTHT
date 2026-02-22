# Environment Setting
from dotenv import load_dotenv
import logging
import os
from pathlib import Path

import RFCallAPI
import RFReadDB
import RFWriteDB

# Endpoints & Environment Variables
load_dotenv()
OpenWeatherEndpoint = 'https://api.openweathermap.org/data/3.0/onecall'
OpenWeatherApiKey = os.getenv('OPENWEATHER_API_KEY')
SupaBaseUrl = os.getenv('SUPABASE_URL')
SupabaseKey = os.getenv('SUPABASE_KEY')

# File Paths
BaseDirectory = Path(__file__).resolve().parent
LogPath = BaseDirectory.parent / 'log'
LogPath.mkdir(parents=True, exist_ok=True)
PipelineLogPath = LogPath / 'PipelineLog.txt'

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', handlers=[logging.FileHandler(PipelineLogPath), logging.StreamHandler()])
logger = logging.getLogger('RetrieveFactsPipeline')

# Run
Cities = RFReadDB.GetCityTable(SupaBaseUrl, SupabaseKey)
FactWeather = RFCallAPI.GetForecastsAndActuals(Cities, OpenWeatherApiKey, OpenWeatherEndpoint, SupaBaseUrl, SupabaseKey)
RFWriteDB.WriteFactWeatherToDatabase(FactWeather, SupaBaseUrl, SupabaseKey)