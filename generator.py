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
    Vytvoř komplexní, vysoce profesionální a vizuálně bohatou jednostránkovou (landing page) webovou stránku pro firmu '{company_name}', která působí v oboru '{industry}'.
    Styl: {style_key}.
    
    ZÁSADNÍ POŽADAVKY:
    1. Použij Tailwind CSS CDN (https://cdn.tailwindcss.com).
    2. Primární barva: {primary_color}. Použij ji pro tlačítka (bg-[{primary_color}]), hover efekty a důležité akcenty.
    3. Typografie: Moderní bezpatkový font (např. Inter nebo sans), velké a výrazné nadpisy, velkorysý padding.
    
    STRUKTURA STRÁNKY (Klíčové pro odstranění prázdného prostoru):
    4. **Hero Sekce (VYPLŇTE OBĚ STRANY):**
       - Musí být dvouciferný grid (grid-cols-2 na desktopech).
       - **Levá strana:** Ponech poutavý nadpis a marketingový text, který prodává hodnotu. Podtext musí mít 3-4 věty. Použij primární barvu pro jedno hlavní CTA tlačítko.
       - **Pravá strana (ZDE MUSÍ BÝT OBSAH):** Vlož **velký visual placeholder**. Například šedý obdélník se zaoblenými rohy a velkou ikonou uprostřed, nebo maketu produktu, která se k tomuto oboru hodí. Tato část nesmí být prázdná.
    
    5. **Navazující Sekce (VYTVOŘ MINIMÁLNĚ 3 DALŠÍ):**
       - **O nás:** Krátký příběh, vize a mise firmy s menším obrázkem.
       - **Služby:** Grid se 3-4 kartami. Každá karta musí mít ikonu, nadpis a podrobnější popis služby (3-4 věty). Použij `shadow-lg` a `rounded-lg`.
       - **Reference/Zákazníci:** Pár příkladů spokojených klientů (loga nebo citace).
       - **Kontakt:** Přehledný kontaktní formulář (placeholder) a kontaktní údaje s malou mapou (placeholder).
    
    6. **Technická Upřesnění:** Web musí být plně responsivní (mobile-first). Do každé sekce doplň profesionální, marketingově laděný text v češtině. Použij hodně vertikálního prostoru (whitespace) mezi sekcemi, ale *ne* prázdný prostor vedle obsahu.
    7. **Vrať POUZE čistý HTML kód bez markdownu a uvozovek.**
    """
    
    return client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_completion_tokens=4000
    )