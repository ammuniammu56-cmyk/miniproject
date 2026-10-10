import streamlit as st

st.set_page_config(
    page_title="Sovereign AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Sovereign AI Assistant")
st.caption("Your private AI workspace")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.write(
            "Your chat interface is working! "
            "We will connect the AI model next."
        )
