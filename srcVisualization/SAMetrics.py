# Environment Setting
import pandas as pd

# Functions | Metrics Calculation & Forecast Evaluation
def FilterDf(df, cities, dataType, dateRange):
    filtered = df[df['City'].isin(cities)]
    filtered = filtered[(filtered['FullTimestamp'].dt.date >= dateRange[0]) & (filtered['FullTimestamp'].dt.date <= dateRange[1])]
    if dataType is not None: filtered = filtered[filtered['DataType'] == dataType]

    return filtered

# Functions | Metrics Calculation
def ComputeWeatherMetrics(df):
    metrics = {}
    columns = {
        'Temperature':       'Temperature',
        'Felt Temperature':  'FeltTemperature',
        'Humidity':          'Humidity',
        'Clouds':            'Clouds',
        'Wind Speed':        'WindSpeed',}
    for label, col in columns.items():
        if col in df.columns:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            metrics[label] = {'Minimum': round(series.min(), 2), 'Average': round(series.mean(), 2), 'Maximum': round(series.max(), 2), 'Standard Deviation': round(series.std(), 2),}
        else: metrics[label] = {'Minimum': None, 'Average': None, 'Maximum': None, 'Standard Deviation': None}
    return metrics

# Functions | Forecast Evaluation
def ComputeForecastAccuracy(df, parameter):
    forecastDf = df[df['DataType'] == 'Forecast'][['City', 'FullTimestamp', parameter]]
    actualDf   = df[df['DataType'] == 'Actual'][['City', 'FullTimestamp', parameter]]
    mergedDf   = forecastDf.merge(actualDf, on=['City', 'FullTimestamp'], suffixes=('_Forecast', '_Actual'))

    actual   = pd.to_numeric(mergedDf[f'{parameter}_Actual'],   errors='coerce')
    forecast = pd.to_numeric(mergedDf[f'{parameter}_Forecast'], errors='coerce')

    mae  = round((actual - forecast).abs().mean(), 2)
    mape = round(((actual - forecast).abs() / actual[actual != 0].abs()).mean() * 100, 2)

    return mae, mape

# Functions | Time Series Comparisons
def PrepareTimeSeriesComparisons(df, parameter, cities):
    actualDf          = df[(df['DataType'] == 'Actual') & (df['City'].isin(cities))][['FullTimestamp', parameter]].rename(columns={parameter: 'Actual'})
    currentForecastDf = df[(df['DataType'] == 'Forecast') & (df['City'].isin(cities))][['FullTimestamp', parameter]].rename(columns={parameter: 'Forecast'})
    mergedDf          = actualDf.merge(currentForecastDf, on='FullTimestamp', how='outer')

    return mergedDf