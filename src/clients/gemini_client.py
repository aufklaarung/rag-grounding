from google.genai import Client, types, errors
from google.api_core import retry

from src.config.settings import GOOGLE_API_KEY

client = Client(api_key=GOOGLE_API_KEY)

@retry.Retry(predicate=lambda e: isinstance(e, errors.APIError) and getattr(e, 'code', None) in {429, 503})
def get_model_response(prompt: str):
    temp_config = types.GenerateContentConfig(temperature=0.2)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=temp_config,
        contents=prompt
    )
    return response.text

