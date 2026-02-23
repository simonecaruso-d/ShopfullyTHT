# Environment Setting
from openai import OpenAI
import streamlit as st

def GenerateLLMComment(mae, mape, parameter, cities, orApiKey, model='qwen/qwen3-vl-30b-a3b-thinking'):
    citiesString = ', '.join(cities)
    
    systemPrompt = """You are a senior meteorological data analyst with expertise in forecast model evaluation. 
                        Your role is to deliver sharp, actionable insights from forecast accuracy metrics, 
                        the kind a data team lead would present in an executive briefing.
                        Rules:
                        - Don't just restate the raw numbers: interpret their meaning and implications;
                        - Be precise but human: avoid jargon unless it adds value;
                        - Highlight what is working, what is concerning, and why it matters;
                        - Max 5 sentences."""

    userPrompt = f"Evaluate the forecast accuracy for the following context. Parameter: {parameter}, Cities monitored: {citiesString}, MAE: {mae}, MAPE: {mape}%. Deliver your insight."

    client = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=orApiKey)
    response = client.chat.completions.create(model=model, max_tokens=150, temperature=0.3, messages=[{'role': 'system', 'content': systemPrompt}, {'role': 'user',   'content': userPrompt}])
    return response.choices[0].message.content