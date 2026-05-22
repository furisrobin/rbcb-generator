import openai
import json
import os
from dotenv import load_dotenv

# Načtení klíče
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_website_data(company_name, industry, style):
    prompt = f"""
    Create a content plan for a company named '{company_name}' in the '{industry}' industry.
    The design style should be '{style}'.
    Return ONLY a valid JSON object with these keys: 
    "slogan", "hero_text", "features" (list of 3 items), "color_palette" (list of 3 hex codes).
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)