import streamlit as st
import time
import os
from google import genai
import markdown
from weasyprint import HTML

st.set_page_config(page_title="Deep Research Agent", page_icon="🔍", layout="centered")
st.title("Autonomous Research Assistant")
st.markdown("Enter a topic below. The agent will autonomously search, cross-reference, and synthesize a comprehensive report.")

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY environment variable is not set. Go to Advanced Settings -> Secrets in Streamlit Cloud.")
    st.stop()

query = st.text_input("Research Topic:", placeholder="e.g., The evolution of CI/CD pipelines in microservice architectures...")

if st.button("Initialize Deep Research", type="primary") and query:
    client = genai.Client(api_key=API_KEY)
    
    with st.spinner("Agent initialized. Planning, searching, and synthesizing. This may take 2-5 minutes..."):
        try:
            interaction = client.interactions.create(
                agent="deep-research-preview-04-2026",
                input=query,
                tools=[{"type": "google_search"}],
                background=True
            )
            
            while True:
                interaction = client.interactions.get(interaction.id)
                
                if interaction.status == "completed":
                    final_report = interaction.output_text

                    html_content = markdown.markdown(final_report)
                    pdf_bytes = HTML(string=html_content).write_pdf()
                    
                    st.success("✅ Research Complete!")
                    
                    st.download_button(
                        label="📄 Download Report as PDF",
                        data=pdf_bytes,
                        file_name="Deep_Research_Report.pdf",
                        mime="application/pdf"
                    )
                    
                    st.markdown("---")
                    st.markdown(final_report)
                    break
                    
                elif interaction.status == "failed":
                    st.error(f"❌ Research task failed: {interaction.error}")
                    break
                else:
                    time.sleep(15)
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
