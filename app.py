
import streamlit as st

st.set_page_config(
    page_title="Sovereign AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: #212121;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #171717;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: #f5f5f5 !important;
}
.stChatInput textarea {
    background: #303030 !important;
    color: white !important;
}
div[data-testid="stFileUploader"] {
    background: #303030;
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = {"New chat": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "New chat"

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🤖 Sovereign AI")
    st.caption("Private AI workspace")
    st.divider()

    if st.button("＋ New chat", use_container_width=True):
        name = f"New chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.rerun()

    st.subheader("Recent chats")

    for name in list(st.session_state.chats.keys()):
        if st.button(name, key=f"chat_{name}", use_container_width=True):
            st.session_state.active_chat = name
            st.session_state.messages = st.session_state.chats[name]
            st.rerun()

    st.divider()
    st.caption("Powered by Streamlit")

# Load selected conversation
if st.session_state.active_chat not in st.session_state.chats:
    st.session_state.chats[st.session_state.active_chat] = []

st.session_state.messages = st.session_state.chats[
    st.session_state.active_chat
]

# ---------- CHAT DISPLAY ----------
if not st.session_state.messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center;'>How can I help you today?</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;color:#aaaaaa !important;'>"
        "Ask a question or attach a file to get started.</p>",
        unsafe_allow_html=True
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("files"):
            st.caption("📎 Attachments: " + ", ".join(message["files"]))

# ---------- ATTACHMENTS ----------
with st.expander("＋ Attach images, videos, PDFs or text files"):
    uploaded_files = st.file_uploader(
        "Choose one or more files",
        type=[
            "png", "jpg", "jpeg", "webp",
            "mp4", "mov", "avi",
            "pdf", "txt", "md", "csv",
            "doc", "docx"
        ],
        accept_multiple_files=True,
        key="attachments"
    )

    if uploaded_files:
        for file in uploaded_files:
            st.caption(f"📎 {file.name} ({file.size / 1024:.1f} KB)")

# ---------- MESSAGE BOX ----------
prompt = st.chat_input("Message Sovereign AI...")

if prompt:
    files = [file.name for file in uploaded_files] if uploaded_files else []

    user_message = {
        "role": "user",
        "content": prompt,
        "files": files
    }

    st.session_state.messages.append(user_message)

    assistant_message = {
        "role": "assistant",
        "content": (
            "Your message has been received! 🤖\n\n"
            "This interface is running, but the AI model is not connected yet. "
            "Next, connect Ollama through the backend to generate real answers."
        )
    }

    st.session_state.messages.append(assistant_message)
    st.rerun()
