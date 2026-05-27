import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

STYLES = {
    "Minimalistický": "Minimalistický design, hodně bílého prostoru, elegantní fonty, jednoduchá navigace.",
    "Moderní": "Moderní vzhled, výrazné barvy, velké nadpisy, dynamické rozložení.",
    "Korporátní": "Profesionální, seriózní vzhled, tmavě modrá/šedá paleta, přehledná struktura.",
    "Technický": "Dark mode, tmavé pozadí, neonové akcenty, monospaced fonty, zaměřeno na data.",
    "Ekologický": "Zaoblené tvary, přírodní paleta (zelené/zemité tóny), organický pocit.",
    "Luxusní": "Vysoký kontrast, patkové písmo (serif), zlaté/černé akcenty, prémiový pocit.",
    "Hravý": "Jasné barvy, zaoblené rohy, hravé animace, energický tón."
}

client = AzureOpenAI(
    azure_endpoint="https://budwise-brigadnici-resource.openai.azure.com",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-15-preview"
)

def generate_website_stream(company_name, industry, style_key, primary_color):
    style_desc = STYLES.get(style_key, "Moderní design.")
    
    prompt = f"""
    Create a complete responsive single-page HTML website for company '{company_name}' in '{industry}' industry.
    Use Tailwind CSS via CDN (https://cdn.tailwindcss.com).
    
    DESIGN SYSTEM:
    - Style: {style_key} ({style_desc})
    - Primary Color: Use '{primary_color}' for primary text, backgrounds, and borders.
    
    REQUIRED SECTIONS (Keep all text extremely short for maximum speed):
    1. Navbar: Brand logo and 3 simple links + 1 CTA button.
    2. Hero: 2-column layout. Left: Short bold title and 1-sentence subtitle. Right: Plain colored visual placeholder box.
    3. Services: Section title + a grid of EXACTLY 3 cards. Each card must have 1 icon, a 2-word title, and a 1-sentence description.
    4. Contact: Simple form placeholder (Name, Email, Send button).
    5. Footer: Short copyright text.
    
    CRITICAL SPEED RULES:
    - Write minimal HTML code (max 100 lines total). No deep nesting. 
    - Output ONLY pure, valid HTML code starting with <html> and closing with </html>. 
    - Absolutely NO markdown codeblocks, NO ```html, NO conversational text.
    """
    return client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_completion_tokens=4000,
    )