import streamlit as st
import google.generativeai as genai

# Set up your Gemini 2.0 Flash API Key
genai.configure(api_key="AIzaSyB1QSrd4XtMAc9zEQZNMc4qTTzAB2WOhbI")  # Make sure to use the appropriate API key

# Load Gemini 2.0 Flash Model
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Set up the app with a general prompt optimizer
st.set_page_config(page_title="OptiPrompt: AI-Driven Prompt Enhancer", page_icon="🤖", layout="wide")  # Layout set to 'wide' for better use of screen
st.title("🤖 OptiPrompt: AI-Powered Prompt Enhancer")

st.markdown("""
Enter a prompt on any topic, get AI-driven optimization, receive actionable insights, 
and choose from multiple optimized versions to see how tweaking can make a big difference.
""")

# Text area for the user's input prompt
user_prompt = st.text_area("✏️ Your Prompt", height=150, placeholder="e.g., Explain quantum computing to a 10-year-old.")

# Placeholder for AI's suggestions and corrections
if "suggestions" not in st.session_state:
    st.session_state.suggestions = ""
if "corrected_prompt" not in st.session_state:
    st.session_state.corrected_prompt = ""

# Layout for the Submit button
submit_clicked = st.button("Submit")

# Few-shot Learning Example Setup
def few_shot_example(prompt):
    examples = """
    Example 1:
    Prompt: "Explain quantum computing."
    Optimized Prompt: "Explain quantum computing in simple terms, avoiding technical jargon, and providing real-world examples."
    
    Example 2: 
    Prompt: "How does AI work?"
    Optimized Prompt: "Describe the process of AI in a way that a beginner can understand, focusing on its key concepts like machine learning and neural networks."
    
    Example 3:
    Prompt: "What is climate change?"
    Optimized Prompt: "Explain the concept of climate change using accessible language, including its causes, effects, and the importance of global action."
    
    Example 4:
    Prompt: "What are the benefits of exercise?"
    Optimized Prompt: "Discuss the physical and mental health benefits of exercise, focusing on the positive impact on both body and mind."

    Please follow this pattern and improve the following prompt for clarity, specificity, and relevance:
    Prompt: "{prompt}"
    """

    return examples.format(prompt=prompt)

# Dynamic suggestions for general prompts
def get_optimized_prompt(prompt):
    if prompt.strip():
        try:
            # Use few-shot learning examples to optimize the prompt
            examples = few_shot_example(prompt)
            # Generate the optimized prompt response using Gemini 2.0 Flash
            optimized_response = model.generate_content(examples)
            return optimized_response.text
        except Exception as e:
            st.error(f"Gemini API Error: {str(e)}")
            return ""
    return ""


# Generate responses for both unoptimized and optimized prompts
def generate_responses(unoptimized_prompt, optimized_prompt):
    try:
        # Generate response for the unoptimized prompt
        unoptimized_response = model.generate_content(unoptimized_prompt)
        
        # Generate response for the optimized prompt
        optimized_response = model.generate_content(optimized_prompt)

        return unoptimized_response.text, optimized_response.text
    except Exception as e:
        st.error(f"Gemini API Error: {str(e)}")
        return None, None

# When Submit is clicked, process the prompt and show both responses
# Checkbox to decide whether to optimize the prompt
optimize = st.checkbox("Optimize my prompt before submission", value=True)

# When Submit is clicked, process the prompt
if submit_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Gemini is thinking..."):

            if optimize:
                # Get optimized prompt
                optimized_prompt = get_optimized_prompt(user_prompt)
                unoptimized_prompt = user_prompt
                
                # Generate both responses
                unoptimized_response, optimized_response = generate_responses(unoptimized_prompt, optimized_prompt)

                # Side-by-side comparison layout
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("📝 Unoptimized Prompt")
                    st.text_area("Original Prompt", unoptimized_prompt, height=150, disabled=True)
                    st.subheader("🧾 Response")
                    st.write(unoptimized_response)

                with col2:
                    st.subheader("📝 Optimized Prompt")
                    st.text_area("Optimized Prompt", optimized_prompt, height=150, disabled=True)
                    st.subheader("🧾 Response")
                    st.write(optimized_response)

                # Optimization Insight
                st.subheader("🔍 Optimization Insights")
                st.write("**Why this optimization works**: The optimized prompt refines your language to be more **specific**, **clear**, and **focused**, which helps the AI produce more accurate and relevant responses.")
            
            else:
                # No optimization — just generate response to the original prompt
                response = model.generate_content(user_prompt)
                
            
                st.subheader("🧾 Response")
                st.write(response.text)
