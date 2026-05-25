import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Slovník stylů pro AI
STYLES = {
    "Minimalistický": "Minimalistický design, hodně bílého prostoru, elegantní fonty, jednoduchá navigace.",
    "Moderní": "Moderní vzhled, výrazné barvy, velké nadpisy, dynamické rozložení.",
    "Korporátní": "Profesionální, seriózní vzhled, tmavě modrá/šedá paleta, přehledná struktura.",
    "Technický": "Dark mode, tmavé pozadí, neonové akcenty, monospaced fonty, zaměřeno na data.",
    "Ekologický": "Zaoblené tvary, přírodní paleta (zelená/zemité tóny), organický pocit.",
    "Luxusní": "Vysoký kontrast, serify (patkové písmo), zlaté/černé akcenty, prémiový pocit.",
    "Hravý": "Jasné barvy, zaoblené rohy, hravé animace, energický tón."
}

client = AzureOpenAI(
    azure_endpoint="https://budwise-brigadnici-resource.openai.azure.com",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview"
)

def generate_website_stream(company_name, industry, style_key):
    deployment_name = "gpt-5"
    style_desc = STYLES.get(style_key, "Moderní čistý design.")
    
    prompt = f"""
    Vytvoř kompletní HTML webovou stránku pro firmu '{company_name}' z oboru '{industry}'.
    Designový styl: {style_key} ({style_desc}).
    Pravidla:
    1. Použij CDN pro Tailwind CSS (https://cdn.tailwindcss.com).
    2. Vytvoř kompletní strukturu: Header, Hero, Služby, Kontakt, Footer.
    3. HTML kód musí být validní a kompletní dokument.
    4. Použij české texty odpovídající oboru.
    5. Vrať POUZE čistý HTML kód, žádné markdown bloky (žádné ```html).
    """
    
    return client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_completion_tokens=4000
    )