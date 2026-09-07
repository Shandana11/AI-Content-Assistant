import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="AI Social Media Content Assistant",
    page_icon="✨",
    layout="centered"
)

st.title("✨ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# Sidebar - API Key input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    help="Get a free API key at https://console.groq.com/keys"
)

# User Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Announcement", "Educational Tip", "Product Promotion", "Story / Reflection"]
        )
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
        )
        
    with col2:
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Engaging & Conversational", "Inspirational", "Direct & Persuasive"]
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Small business owners, Designers, Tech enthusiasts"
        )
    
    topic = st.text_area(
        "Topic / Key Message",
        placeholder="e.g., How to use color theory in logo design to attract clients...",
        height=100
    )
    
    submit_button = st.form_submit_button("Generate Post 🚀")

# Generation Logic
if submit_button:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            prompt = f"""
            You are an expert social media content creator and copywriter.
            Generate a high-converting {content_type} specifically tailored for {platform}.
            
            Key Inputs:
            - Topic/Message: {topic}
            - Target Audience: {target_audience}
            - Tone of Voice: {tone}
            
            Please provide the response in the following structured layout:
            
            1. **Main Content/Body**: The core post optimized for {platform}'s best practices (formatting, line breaks, hook).
            2. **Call to Action (CTA)**: A compelling CTA encouraging engagement.
            3. **Hashtags**: 5 to 8 relevant, high-impact hashtags.
            """
            
            with st.spinner("Generating your post..."):
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )
                
                generated_text = response.choices[0].message.content
                
                st.success("Content Generated Successfully!")
                st.subheader("Your Generated Post")
                st.markdown(generated_text)
                
                # Allow user to download the generated post
                st.download_button(
                    label="Download Post as Text File",
                    data=generated_text,
                    file_name="generated_post.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")