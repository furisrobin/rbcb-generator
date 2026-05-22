import streamlit as st
import streamlit.components.v1 as components
import base64
from generator import generate_website_stream

st.set_page_config(page_title="RBCB Generátor", layout="wide")
st.title("🚀 RBCB - AI Webový Architekt")

# Inicializace stavu (aby kód nezmizel)
if 'full_code' not in st.session_state:
    st.session_state.full_code = None

with st.sidebar:
    company_name = st.text_input("Název firmy")
    industry = st.text_input("Obor")
    style = st.selectbox("Styl", ["Minimalistický", "Moderní", "Korporátní"])
    generate_btn = st.button("Generovat web")

# Pokud bylo kliknuto na generování, spustíme proces
if generate_btn and company_name and industry:
    st.session_state.full_code = "" # Reset před novým generováním
    st.subheader("Generuji kód...")
    code_placeholder = st.empty()
    
    stream = generate_website_stream(company_name, industry, style)
    
    for chunk in stream:
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                st.session_state.full_code += delta.content
                code_placeholder.code(st.session_state.full_code, language="html")

# --- Zobrazení, pokud máme kód v paměti (i po kliknutí na stažení) ---
if st.session_state.full_code:
    # Očištění
    clean_code = st.session_state.full_code.replace("```html", "").replace("```", "").strip()
    
    # Validace HTML kostry
    if "<html>" not in clean_code.lower():
        final_html = f"<!DOCTYPE html><html><body>{clean_code}</body></html>"
    else:
        final_html = clean_code
        
    st.success("Web vygenerován!")
    
    # Tlačítka
    b64 = base64.b64encode(final_html.encode()).decode()
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Stáhnout HTML", data=final_html, file_name="index.html", mime="text/html")
    with col2:
        st.markdown(f'<a href="data:text/html;base64,{b64}" target="_blank" style="...">🌐 Otevřít web</a>', unsafe_allow_html=True)

    st.subheader("Náhled v aplikaci:")
    components.iframe(src=f"data:text/html;base64,{b64}", height=600)