import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Page Configuration
st.set_page_config(page_title="SkillGap Architect | ALTA Fellowship", page_icon="🚀", layout="wide")

# 2. Robust API Key Access
# This prevents the crash if secrets.toml is missing locally
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    else:
        st.sidebar.info("Secret key not found. Please use the manual input.")
except Exception:
    # If st.secrets doesn't exist at all (local dev without folder)
    st.sidebar.info("Running in local mode. Enter API key below.")

# Manual input fallback in sidebar
user_key = st.sidebar.text_input("Gemini API Key", type="password", help="Get your key from aistudio.google.com")
if user_key:
    os.environ["GOOGLE_API_KEY"] = user_key

# 3. UI Styling & Headers
st.title("🚀 SkillGap Architect")
st.subheader("RAG-Powered Agentic Career Roadmap Generator")
st.markdown("""
    **Assignment 1 (RAG) & Assignment 2 (Agentic Tool) Submission**  
    *Analyze your resume, identify 2026 industry gaps, and build a learning sprint.*
""")
st.markdown("---")

# 4. Inputs: Resume (RAG) & Job Goal
col1, col2 = st.columns([1, 1])

with col1:
    st.write("### 📄 Step 1: Upload Profile")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")

with col2:
    st.write("### 🎯 Step 2: Set Goal")
    target_job = st.text_input("Target Job Role", placeholder="e.g., MERN Stack Developer")
    experience_level = st.selectbox("Current Level", ["Student/Fresher", "Junior", "Mid-Level"])

# 5. The Logic
if st.button("🚀 Build My Career Roadmap") and uploaded_file and target_job:
    if not os.environ.get("GOOGLE_API_KEY"):
        st.error("🔑 Error: Missing API Key! Please enter it in the sidebar.")
    else:
        with st.spinner("🧠 Agent is analyzing your resume against 2026 industry standards..."):
            try:
                # Save and Load PDF (RAG Implementation)
                with open("temp_resume.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                loader = PyPDFLoader("temp_resume.pdf")
                pages = loader.load_and_split()
                resume_text = " ".join([p.page_content for p in pages])

                # Initialize LLM (Gemini 1.5 Flash)
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

                # Agentic Prompting Logic
                agent_prompt = f"""
                You are a Career Architect AI Assistant. 
                User's Current Resume Content: {resume_text}
                Goal: Become a {target_job} at a top-tier technology company.
                User Level: {experience_level}
                
                Based on the provided resume context (RAG), perform a strategic GAP ANALYSIS:
                1. **Skill Gap Analysis**: What 3 specific technical skills or tools are missing for a {target_job} role in 2026?
                2. **4-Week Learning Sprint**: Create a structured, week-by-week plan to learn these skills.
                3. **High-Impact Project**: Suggest ONE project that bridges their current skills with the gaps.
                4. **LinkedIn Optimization**: Write a 2-sentence 'About' summary based on this roadmap.
                
                Format the response with professional Markdown, bold headings, and clean bullet points.
                """

                response = llm.invoke(agent_prompt)

                # 6. Display Results
                st.success("✅ Analysis Complete!")
                st.markdown("---")
                st.markdown(response.content)
                
                # Bonus Feature: Download result as text
                st.download_button(
                    label="📥 Download Roadmap as Text",
                    data=response.content,
                    file_name=f"{target_job}_Roadmap.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"⚠️ Technical Error: {e}")

else:
    if not uploaded_file or not target_job:
        st.info("💡 Getting Started: Please upload your Resume (PDF) and enter your dream Job Role.")

# Footer for Fellowship
st.markdown("---")
st.caption("Developed by Maddi Venkata Teja | ANITS 2027 | ALTA AI Builders Fellowship")