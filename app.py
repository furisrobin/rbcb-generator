import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import os
from generator import generate_website_stream

# Konfigurace
st.set_page_config(page_title="RBCB Generátor", layout="wide")
HISTORY_FILE = "history.json"

# Funkce pro historii
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip(): # Pokud je soubor prázdný
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            # Pokud je soubor poškozený, raději ho resetujeme na prázdný seznam
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Inicializace stavu
if 'history' not in st.session_state:
    st.session_state.history = load_history()
if 'current_code' not in st.session_state:
    st.session_state.current_code = None

st.title("🚀 RBCB - AI Webový Architekt")

# Sidebar
with st.sidebar:
    st.header("Nastavení")
    company_name = st.text_input("Název firmy")
    industry = st.text_input("Obor")
    style = st.selectbox("Styl", ["Minimalistický", "Moderní", "Korporátní"])
    generate_btn = st.button("Generovat nový web")
    
    st.divider()
    st.header("📜 Historie")
    for i, item in enumerate(st.session_state.history):
        if st.button(f"Web: {item['name']}", key=f"hist_{i}"):
            st.session_state.current_code = item['code']

# Generování
if generate_btn and company_name and industry:
    st.session_state.current_code = "" 
    
    with st.spinner('AI kreslí váš web...'):
        code_placeholder = st.empty()
        full_code = ""
        
        stream = generate_website_stream(company_name, industry, style)
        
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full_code += delta.content
                    code_placeholder.code(full_code, language="html")
        
        st.session_state.current_code = full_code
        new_entry = {'name': company_name, 'code': full_code}
        st.session_state.history.append(new_entry)
        save_history(st.session_state.history)
    
    st.rerun() 

# Vykreslení
if st.session_state.current_code:
    clean_code = st.session_state.current_code.replace("```html", "").replace("```", "").strip()
    final_html = clean_code if "<html>" in clean_code.lower() else f"<!DOCTYPE html><html><body>{clean_code}</body></html>"
    
    st.success("Web připraven!")
    st.download_button("📥 Stáhnout HTML", data=final_html, file_name="index.html", mime="text/html")

    st.markdown("---")
    st.subheader("Náhled v aplikaci:")
    b64 = base64.b64encode(final_html.encode()).decode()
    components.iframe(src=f"data:text/html;base64,{b64}", height=600)