import streamlit as st
import google.generativeai as genai

# Set your Gemini API key here
genai.configure(api_key="AIzaSyB1QSrd4XtMAc9zEQZNMc4qTTzAB2WOhbI")  # Replace with your actual API key

# Load the Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Set up Streamlit app
st.set_page_config(page_title="ChronoPrompt", page_icon="🤖")
st.title("ChronoPrompt: Smart Prompt Optimizer")
st.markdown("Enter a prompt, get smart improvement suggestions, auto-correct it, and submit to see the final result.")

# Text input for prompt
user_prompt = st.text_area("✏️ Your Prompt", height=150, placeholder="e.g., Explain quantum computing to a 10-year-old.")

# Initialize session state to store suggestion + corrected prompt
if "suggestions" not in st.session_state:
    st.session_state.suggestions = ""
if "corrected_prompt" not in st.session_state:
    st.session_state.corrected_prompt = ""

# Layout: 2 buttons side by side
col1, col2 = st.columns([1, 1])

with col1:
    prompt_check_clicked = st.button("🔍 Prompt Checker")

with col2:
    submit_clicked = st.button("Submit Prompt")

# Logic for Prompt Checker
if prompt_check_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Gemini analyzing your prompt..."):
            try:
                response = model.generate_content(
                    f"Suggest improvements to the following prompt for clarity, specificity, and relevance:\n\n{user_prompt}"
                )
                st.session_state.suggestions = response.text
                st.subheader("✅ Suggested Improvements")
                st.write(st.session_state.suggestions)

                if st.button("✨ Auto-Correct This Prompt"):
                    correction = model.generate_content(
                        f"Rewrite this prompt using the suggestions above: {user_prompt}"
                    )
                    st.session_state.corrected_prompt = correction.text
                    st.subheader("🔁 Auto-Corrected Prompt")
                    st.text_area("Updated Prompt", st.session_state.corrected_prompt, height=150)

            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")

# Logic for Submit Prompt
if submit_clicked:
    prompt_to_submit = st.session_state.corrected_prompt or user_prompt

    if not prompt_to_submit.strip():
        st.warning("Please enter a prompt or generate a corrected one first.")
    else:
        with st.spinner("Gemini is generating your final response..."):
            try:
                final_response = model.generate_content(prompt_to_submit)
                st.subheader("🧾 Gemini's Response to Your Prompt")
                st.write(final_response.text)
            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")
