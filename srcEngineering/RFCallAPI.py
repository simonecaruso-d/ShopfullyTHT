# Environment Setting
from datetime import datetime, timezone, timedelta
import pandas as pd
from tqdm import tqdm

import RFHelpers

# Functions | Get Fact Tables
def GetForecast(citiesDf, owApiKey, owBaseEndpoint):
    rows = []
    nowUtc = datetime.now(timezone.utc)

    for _, row in tqdm(citiesDf.iterrows(), total=citiesDf.shape[0], desc='Processing cities (Forecast)'):
        lat        = row['Latitude']
        lon        = row['Longitude']
        cityId     = row['Id']
        parameters = {'lat': lat, 'lon': lon, 'units': 'metric', 'exclude': 'current,minutely,daily,alerts', 'appid': owApiKey}

        hourlyData = RFHelpers.FetchData(owBaseEndpoint, parameters)
        for hour in hourlyData['hourly']: rows.append(RFHelpers.ParseHourlyData(hour, cityId, nowUtc))

    df             = pd.DataFrame(rows)
    df['DataType'] = 'Forecast'
    return df

def GetHistorical(citiesDf, owApiKey, owBaseEndpoint):
    rows   = []
    nowUtc = datetime.now(timezone.utc)

    for _, row in tqdm(citiesDf.iterrows(), total=citiesDf.shape[0], desc='Processing cities (Historical)'):
        lat    = row['Latitude']
        lon    = row['Longitude']
        cityId = row['Id']

        for daysAgo in range(1, 4):
            for hour in range(24):
                dateTime   = nowUtc - timedelta(days=daysAgo, hours=nowUtc.hour - hour)
                timestamp  = int(dateTime.timestamp())
                endpoint   = f'{owBaseEndpoint}/timemachine'
                parameters = {'lat': lat, 'lon': lon, 'dt': timestamp, 'units': 'metric', 'appid': owApiKey}
                data       = RFHelpers.FetchData(endpoint, parameters)
                for hour in data['data']: rows.append(RFHelpers.ParseHourlyData(hour, cityId, nowUtc))

    df             = pd.DataFrame(rows)
    df['DataType'] = 'Actual'
    return df

def GetForecastsAndActuals(citiesDf, owApiKey, owBaseEndpoint):
    forecasts            = GetForecast(citiesDf, owApiKey, owBaseEndpoint)
    actuals              = GetHistorical(citiesDf, owApiKey, owBaseEndpoint)
    combinedData         = pd.concat([actuals, forecasts], ignore_index=True)
    combinedData['CTId'] = combinedData['CTId'].astype(int)
    combinedData['WCId'] = combinedData['WCId'].astype(int)

    return combinedData