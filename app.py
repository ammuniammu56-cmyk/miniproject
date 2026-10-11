
import streamlit as st

st.set_page_config(
    page_title="Sovereign AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: #212121;
    color: #f5f5f5;
}
[data-testid="stSidebar"] {
    background: #171717;
    border-right: 1px solid #303030;
}
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}
h1, h2, h3, p, label {
    color: #f5f5f5;
}
div.stButton > button {
    border-radius: 10px;
    border: 1px solid #454545;
    background: #252525;
    color: white;
}
div.stButton > button:hover {
    border-color: #888;
    color: white;
}
[data-testid="stChatMessage"] {
    border-radius: 14px;
}
[data-testid="stChatInput"] {
    background: #303030;
    border-radius: 16px;
}
[data-testid="stFileUploader"] {
    background: #262626;
    border-radius: 12px;
    padding: 10px;
}
.small-muted {
    text-align: center;
    color: #a0a0a0;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION DATA ----------
if "chats" not in st.session_state:
    st.session_state.chats = {"New chat": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "New chat"

if "pending_files" not in st.session_state:
    st.session_state.pending_files = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🤖 Sovereign AI")
    st.caption("Your private AI workspace")

    if st.button("＋  New chat", use_container_width=True):
        name = f"New chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.session_state.pending_files = []
        st.rerun()

    st.divider()
    st.subheader("Recent chats")

    for name in list(st.session_state.chats.keys())[::-1]:
        if st.button(
            name,
            key=f"select_{name}",
            use_container_width=True,
        ):
            st.session_state.active_chat = name
            st.session_state.pending_files = []
            st.rerun()

    st.divider()
    st.caption("Local-first AI • Private workspace")

# ---------- CURRENT CHAT ----------
messages = st.session_state.chats[st.session_state.active_chat]

if not messages:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center;'>"
        "How can I help you today?</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='small-muted'>Ask a question or attach a file.</p>",
        unsafe_allow_html=True,
    )

# ---------- DISPLAY MESSAGES ----------
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("files"):
            st.caption("📎 " + ", ".join(message["files"]))

# ---------- ATTACH FILES ----------
with st.expander("＋ Attach images, videos, PDFs or text files"):
    new_files = st.file_uploader(
        "Choose your files",
        type=[
            "png", "jpg", "jpeg", "webp",
            "mp4", "mov", "avi",
            "pdf", "txt", "md", "csv",
            "doc", "docx",
        ],
        accept_multiple_files=True,
        key="file_upload",
    )

    if new_files:
        st.session_state.pending_files = new_files
        for file in new_files:
            st.caption(f"📎 {file.name}")

# ---------- SEND MESSAGE ----------
prompt = st.chat_input("Message Sovereign AI...")

if prompt:
    files = [
        file.name for file in st.session_state.pending_files
    ]

    messages.append({
        "role": "user",
        "content": prompt,
        "files": files,
    })

    messages.append({
        "role": "assistant",
        "content": (
            "Thanks! Your message has been received. 🤖\n\n"
            "**Demo mode:** The interface is working, but a real AI "
            "model has not been connected yet. We can connect Ollama "
            "next to generate intelligent answers."
        ),
    })

    st.session_state.pending_files = []
    st.rerun()
