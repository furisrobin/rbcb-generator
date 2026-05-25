import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import os
from generator import generate_website_stream, STYLES

st.set_page_config(page_title="RBCB - AI Webový Architekt", layout="wide")
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                return json.loads(content) if content.strip() else []
        except: return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

if 'history' not in st.session_state: st.session_state.history = load_history()
if 'current_code' not in st.session_state: st.session_state.current_code = None

st.title("🚀 RBCB - AI Webový Architekt")

with st.sidebar:
    st.header("Nastavení")
    company_name = st.text_input("Název firmy")
    industry = st.text_input("Obor")
    style = st.selectbox("Styl", list(STYLES.keys()))
    generate_btn = st.button("Generovat nový web")
    
    st.divider()
    st.header("📜 Historie")
    for i, item in enumerate(st.session_state.history):
        if st.button(f"Web: {item['name']}", key=f"hist_{i}"):
            st.session_state.current_code = item['code']

if generate_btn and company_name and industry:
    with st.spinner('AI kreslí váš web...'):
        code_placeholder = st.empty()
        full_code = ""
        stream = generate_website_stream(company_name, industry, style)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                full_code += chunk.choices[0].delta.content
                code_placeholder.code(full_code, language="html")
        
        st.session_state.current_code = full_code
        st.session_state.history.append({'name': company_name, 'code': full_code})
        save_history(st.session_state.history)
        st.rerun()

if st.session_state.current_code:
    # Sekce pro editaci
    with st.expander("✏️ Upravit kód ručně"):
        edited_code = st.text_area("HTML kód:", value=st.session_state.current_code, height=300)
        if st.button("🔄 Aktualizovat náhled"):
            st.session_state.current_code = edited_code
            st.rerun()

    st.success("Web je připraven!")
    st.download_button("📥 Stáhnout HTML", data=st.session_state.current_code, file_name="index.html", mime="text/html")

    st.markdown("---")
    st.subheader("Náhled v aplikaci:")
    b64 = base64.b64encode(st.session_state.current_code.encode()).decode()
    components.iframe(src=f"data:text/html;base64,{b64}", height=600)