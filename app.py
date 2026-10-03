import streamlit as st
from google import genai
from prompts import SYSTEM_PROMPT
st.set_page_config(
    page_title="SnapStudy AI",
    page_icon="📚",
    layout="centered"
)

# Gemini client
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash"

st.title("📸 SnapStudy AI")
st.write("Upload a question, diagram, or notes and get a simple explanation.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload your question or notes",
    type=["png", "jpg", "jpeg", "webp", "pdf"]
)

question = st.text_area(
    "Or type your question here:",
    placeholder="Example: Explain photosynthesis in simple words..."
)

if st.button("✨ Explain"):

    if uploaded_file is None and not question.strip():
        st.warning("Please upload a file or type a question first.")

    else:
        with st.spinner("🤖 Thinking..."):

            try:
                parts = [SYSTEM_PROMPT]

                if question.strip():
                    parts.append(question)

                if uploaded_file is not None:
                    file_bytes = uploaded_file.getvalue()

                    parts.append(
                        {
                            "inline_data": {
                                "mime_type": uploaded_file.type,
                                "data": file_bytes
                            }
                        }
                    )

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=parts
                )

                st.subheader("📖 Explanation")
                st.write(response.text)

            except Exception as error:
                st.error(f"Something went wrong: {error}")