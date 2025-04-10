import streamlit as st
import requests
from bot import process_message

# URL da sua API FastAPI
#API_URL = "http://localhost:8000/chat/"

# Título
st.set_page_config(page_title="Chat com IA", layout="wide")
st.title("Chat Eng IA")

# Inicializa o histórico do chat na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        resposta = process_message(prompt) #requests.post(API_URL, json={"user": "Usuário", "message": prompt})
    except Exception as e:
        resposta = {"message":f"Erro ao conectar à IA: {e}"}

    # Adiciona resposta no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta["message"]})
    with st.chat_message("assistant"):
        st.markdown(resposta["message"])
