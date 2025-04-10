import streamlit as st
from openai import AzureOpenAI
from keployrag.config import (
    AZURE_OPENAI_API_KEY, 
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_CHAT_DEPLOYMENT
)
from prompt_flow import execute_rag_flow

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

st.title("KeployRAG: Your Coding Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your coding question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = execute_rag_flow(prompt)
            message_placeholder.markdown(response)
            full_response = response
        except Exception as e:
            error_message = f"Error in RAG flow execution: {str(e)}"
            st.error(error_message)
            full_response = error_message

    st.session_state.messages.append({"role": "assistant", "content": full_response})
