import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

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

def generate_website_stream(company_name, industry, style_key, primary_color):
    prompt = f"""
    Vytvoř špičkovou, profesionální webovou stránku pro '{company_name}' ({industry}).
    Styl: {style_key}.
    
    POŽADAVKY:
    1. Použij Tailwind CSS CDN (https://cdn.tailwindcss.com).
    2. Primární barva: {primary_color}. Použij ji pro tlačítka (class="bg-[{primary_color}]") a akcenty.
    3. Typografie: Moderní bezpatkový font, velké tučné nadpisy, velkorysý padding a mezery.
    4. Struktura: Navbar, Hero (vlevo text, vpravo placeholder), Služby (karty), Kontakt, Footer.
    5. Vrať POUZE čistý HTML kód bez markdownu a uvozovek.
    """
    
    return client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_completion_tokens=4000
    )