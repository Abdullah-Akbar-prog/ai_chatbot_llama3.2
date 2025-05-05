import streamlit as st
import requests

st.set_page_config(page_title="LLaMA 3 Chatbot", layout="centered")
st.title("🦙 LLaMA 3.2 Chatbot (Local)")
st.write("Ask your legal question related to tenants, consumers, or cyber laws:")
st.write (
        "You are an AI Legal Advisor. Provide general legal information only. "
        "Specialize in consumer rights, tenant rights, and cyber laws. "
        "Always include this disclaimer at the end: "
        "'Disclaimer: This is for informational purposes only and does not constitute legal advice.'"
    )
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You : ", "")

if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Send to local ollama server
    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.2",
        "messages": st.session_state.chat_history,
        "stream": False
    })

    if response.ok:
        data = response.json()
        reply = data['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    else:
        reply = "⚠️ Error: Unable to get response from LLaMA."

# Display chat history
for chat in st.session_state.chat_history:
    speaker = "You" if chat["role"] == "user" else "LLaMA"
    st.markdown(f"**{speaker}:** {chat['content']}")
