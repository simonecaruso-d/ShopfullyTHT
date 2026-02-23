# Environment Setting
from openai import OpenAI
import streamlit as st

def GenerateLLMComment(mae, mape, parameter, cities, orApiKey, model='openai/gpt-4o-mini'):
    citiesString = ', '.join(cities)
    prompt = (
        f"""You are a data analyst commenting on weather forecast accuracy metrics for a dashboard.
            Be concise (2-3 sentences), professional, and insightful. Do not repeat the numbers back literally — interpret them.\n\n
            Parameter: {parameter}\n
            Cities: {citiesString}\n
            MAE: {mae}\n
            MAPE: {mape}%\n\n
            Write a short analytical comment on the forecast quality for this parameter and these cities.""")
    client = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=orApiKey)
    response = client.chat.completions.create(model=model, max_tokens=150, messages=[{'role': 'user', 'content': prompt}])
    return response.choices[0].message.content