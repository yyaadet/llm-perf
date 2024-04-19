import streamlit as st
import ollama
from typing import Dict, Generator


def ollama_generator(model_name: str, messages: Dict) -> Generator:
    stream = ollama.chat(model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk['message']['content']


st.title("行恒编程1对1 - AI聊天机器人")

if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.selected_model = st.selectbox(
    "请先选择模型:", [model["name"] for model in ollama.list()["models"]])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("让我来帮你?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "system", "content": '用中文来回答如下问题'})
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(ollama_generator(
            st.session_state.selected_model, st.session_state.messages))
    st.session_state.messages.append(
        {"role": "assistant", "content": response})