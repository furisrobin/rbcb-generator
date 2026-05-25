import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import os
from generator import generate_website_stream, STYLES

st.set_page_config(page_title="RBCB - AI Architect", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    div.stButton > button { border-radius: 8px; width: 100%; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, ensure_ascii=False, indent=4)

if 'history' not in st.session_state: st.session_state.history = load_history()
if 'current_code' not in st.session_state: st.session_state.current_code = None

with st.sidebar:
    st.title("⚙️ Nastavení")
    company_name = st.text_input("Název firmy")
    industry = st.text_input("Obor")
    style = st.selectbox("Styl designu", list(STYLES.keys()))
    primary_color = st.color_picker("Primární barva", "#3b82f6")
    generate_btn = st.button("🚀 Generovat web")
    
    st.divider()
    st.subheader("📜 Historie")
    for i, item in enumerate(st.session_state.history):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(item['name'], key=f"h_{i}"): st.session_state.current_code = item['code']
        with col2:
            if st.button("🗑️", key=f"d_{i}"):
                st.session_state.history.pop(i)
                save_history(st.session_state.history)
                st.rerun()

st.title("🚀 RBCB - AI Webový Architekt")

# Generovací logika s okamžitým vymazáním statusu
if generate_btn and company_name and industry:
    status_placeholder = st.empty()
    with status_placeholder:
        with st.status("AI kreslí váš web...", expanded=True) as status:
            code_placeholder = st.empty()
            full_code = ""
            stream = generate_website_stream(company_name, industry, style, primary_color)
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_code += chunk.choices[0].delta.content
                    code_placeholder.code(full_code, language="html")
    
    # Úplné vymazání celého status bloku
    status_placeholder.empty()
    
    st.session_state.current_code = full_code
    st.session_state.history.append({'name': company_name, 'code': full_code})
    save_history(st.session_state.history)
    st.rerun()

# Zobrazení výsledku
if st.session_state.current_code:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.download_button("📥 Stáhnout HTML", data=st.session_state.current_code, file_name="index.html")
    
    with st.expander("✏️ Ruční úprava kódu"):
        edited_code = st.text_area("HTML kód:", value=st.session_state.current_code, height=300)
        if st.button("🔄 Aktualizovat náhled"):
            st.session_state.current_code = edited_code
            st.rerun()
    
    st.subheader("Náhled v aplikaci")
    b64 = base64.b64encode(st.session_state.current_code.encode()).decode()
    components.iframe(src=f"data:text/html;base64,{b64}", height=600)
    st.markdown('</div>', unsafe_allow_html=True)