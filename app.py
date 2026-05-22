import streamlit as st
from generator import generate_website_data

st.set_page_config(page_title="RBCB Generator")
st.title("🚀 RBCB - AI Website Generator")

company_name = st.text_input("Company Name")
industry = st.text_input("Industry")
style = st.selectbox("Style", ["Minimalist", "Modern", "Corporate"])

if st.button("Generate"):
    if company_name and industry:
        with st.spinner("AI is working..."):
            try:
                data = generate_website_data(company_name, industry, style)
                st.success("Generated successfully!")
                st.write(f"### Slogan: {data['slogan']}")
                st.write(f"**Hero text:** {data['hero_text']}")
                st.write("### Features:")
                for feature in data['features']:
                    st.write(f"- {feature}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please fill in Company Name and Industry.")