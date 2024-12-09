import streamlit as st
from groq import Groq
import os

# Set page config
st.set_page_config(page_title="هوش مصنوعی داستان سرا", layout="wide")
os.environ["GROQ_API_KEY"] = "YOUR-API-KEY"

# Initialize Groq client
client = Groq()

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("هوش مصنوعی داستان سرای کیارش خاندانی")

# Sidebar for model selection
model = st.sidebar.selectbox(
    "Select Model",
    ["gemma2-9b-it", "llama-3.1-70b-versatile"]
)

# Chat interface
st.write("هوش مصنوعی داستان سرا")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("بگویید چه داستانی  می خواهید؟"):
    st.session_state.messages.append({"role": "system", "content": "You are a science teacher. Answer science questions in an engaging and accurate way in Persian."})

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from Groq
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages
            )
            response = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
