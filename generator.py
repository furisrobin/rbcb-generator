import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


client = AzureOpenAI(
    azure_endpoint="https://budwise-brigadnici-resource.openai.azure.com",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview"
)

def generate_website_stream(company_name, industry, style):
    deployment_name = "gpt-5"
    
    prompt = f"""
    Vytvoř HTML webovou stránku pro '{company_name}'.
    Styl: {style}.
    Pravidla:
    1. Vrať pouze kód, žádné textové uvozování.
    2. Použij velmi stručné CSS v <style> tagu.
    3. HTML musí být validní a kompletní dokument.
    4. Kód musí být ukončený tagem </html>.
    """
    
    return client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_completion_tokens=4000
    )