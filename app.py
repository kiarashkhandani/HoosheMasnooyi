#Kiarash Khandani's Nofanfest Project
import streamlit as st
from groq import Groq
import os

# Set page config
st.set_page_config(page_title="هوش مصنوعی  کمک آموزشی", layout="wide")
#os.environ["GROQ_API_KEY"] = "YOUR-API-KEY"

# Initialize Groq client
client = Groq()

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title
st.title("هوش مصنوعی کمک آموزشی کیارش خاندانی")

# Sidebar for model selection
model = st.sidebar.selectbox(
    "Select Model",
    ["gemma2-9b-it", "llama-3.1-70b-versatile"]
)

# Chat interface
st.write("هوش مصنوعی کمک آموزشی")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("سوالات خود را بپرسید"):
    st.session_state.messages.append({"role": "system", "content": "You are an exceptionally good science teacher.You answer science questions in an accurate and accessible way in Persian."})

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
