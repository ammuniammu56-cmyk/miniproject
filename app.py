import streamlit as st
from uuid import uuid4
from datetime import datetime
import time

# =========================
# App configuration
# =========================
st.set_page_config(
    page_title="Sovereign AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Constants
# =========================
SUPPORTED_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".mp4", ".doc", ".docx", ".txt"
}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: #0b0b0f;
            color: #f3f4f6;
        }

        [data-testid="stSidebar"] {
            background: #111318;
            border-right: 1px solid #1f2937;
        }

        .sidebar-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 0.5rem;
        }

        .sidebar-label {
            color: #94a3b8;
            font-size: 0.8rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        .new-chat-button {
            width: 100%;
            background: #1f2937 !important;
            color: white !important;
            border: 1px solid #374151 !important;
            border-radius: 10px !important;
            padding: 0.7rem 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important;
        }

        .history-button {
            width: 100%;
            background: transparent !important;
            color: #e2e8f0 !important;
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            padding: 0.55rem 0.75rem !important;
            text-align: left !important;
            margin-bottom: 0.35rem !important;
        }

        .history-button:hover {
            background: #1f2937 !important;
            border-color: #374151 !important;
        }

        .settings-button {
            width: 100%;
            background: transparent !important;
            color: #f8fafc !important;
            border: 1px solid #374151 !important;
            border-radius: 10px !important;
            padding: 0.6rem 0.75rem !important;
            margin-top: 0.5rem !important;
        }

        .chat-shell {
            min-height: calc(100vh - 100px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #0b0b0f;
        }

        .message-area {
            flex: 1;
            overflow-y: auto;
            padding: 1rem 1.5rem 0.5rem 1.5rem;
            background: #0b0b0f;
        }

        .empty-state {
            height: 70vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #9ca3af;
        }

        .empty-logo {
            font-size: 2.6rem;
            font-weight: 700;
            color: #68d391;
            margin-bottom: 0.5rem;
        }

        .empty-title {
            font-size: 1.2rem;
            color: #f8fafc;
        }

        .message-row {
            display: flex;
            margin-bottom: 1rem;
            animation: fadein 0.28s ease-in;
        }

        @keyframes fadein {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .user-row {
            justify-content: flex-end;
        }

        .assistant-row {
            justify-content: flex-start;
        }

        .bubble {
            max-width: 72%;
            border-radius: 18px;
            padding: 0.9rem 1rem;
            line-height: 1.55;
            font-size: 0.98rem;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .user-bubble {
            background: linear-gradient(135deg, #10a37f, #0f766e);
            color: white;
            border-bottom-right-radius: 6px;
        }

        .assistant-bubble {
            background: #1f2937;
            color: #f3f4f6;
            border: 1px solid #374151;
            border-bottom-left-radius: 6px;
        }

        .attachment-list {
            margin-top: 0.55rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        .attachment-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(255,255,255,0.08);
            color: #d1d5db;
            border: 1px solid #4b5563;
            border-radius: 999px;
            padding: 0.25rem 0.55rem;
            font-size: 0.75rem;
        }

        .demo-banner {
            background: rgba(251, 191, 36, 0.1);
            border: 1px solid rgba(251, 191, 36, 0.5);
            color: #fbbf24;
            border-radius: 10px;
            padding: 0.6rem 0.75rem;
            margin-bottom: 0.6rem;
            font-size: 0.86rem;
            font-weight: 600;
        }

        .composer {
            position: sticky;
            bottom: 0;
            background: #0b0b0f;
            border-top: 1px solid #1f2937;
            padding: 1rem 1.2rem 1.2rem 1.2rem;
        }

        .composer-box {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 18px;
            padding: 0.55rem 0.7rem 0.6rem 0.7rem;
            box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        }

        .prompt-input {
            background: transparent;
            color: #f8fafc;
            border: none;
            width: 100%;
            font-size: 1rem;
            resize: none;
            min-height: 54px;
            max-height: 200px;
        }

        .prompt-input::placeholder {
            color: #94a3b8;
        }

        .prompt-input:focus {
            outline: none;
            box-shadow: none;
        }

        .send-button {
            background: #10a37f !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            min-width: 56px !important;
            width: 56px !important;
            height: 42px !important;
            padding: 0 !important;
            margin-left: 0.5rem !important;
        }

        .upload-box {
            background: #121821;
            border: 1px dashed #374151;
            border-radius: 12px;
            padding: 0.8rem;
            margin-bottom: 0.8rem;
        }

        .upload-title {
            color: #d1d5db;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }

        .upload-helper {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }

        .file-list {
            margin-top: 0.7rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }

        .file-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 10px;
            padding: 0.55rem 0.7rem;
            color: #e5e7eb;
        }

        .file-meta {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            overflow: hidden;
        }

        .file-name {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .remove-file {
            background: transparent !important;
            color: #fca5a5 !important;
            border: none !important;
            font-size: 1rem !important;
            padding: 0.2rem 0.4rem !important;
        }

        .error-banner {
            background: rgba(127, 29, 29, 0.4);
            border: 1px solid rgba(239, 68, 68, 0.7);
            color: #fca5a5;
            border-radius: 10px;
            padding: 0.7rem 0.9rem;
            margin-bottom: 0.6rem;
            font-size: 0.85rem;
        }

        .small-muted {
            color: #9ca3af;
            font-size: 0.8rem;
        }

        .stFileUploader label {
            color: #e5e7eb !important;
        }

        .stButton > button {
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            filter: brightness(1.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Helper functions
# =========================
def make_new_chat():
    new_id = str(uuid4())
    return {
        "id": new_id,
        "title": "New chat",
        "created_at": datetime.utcnow().isoformat(),
        "messages": [],
    }


def get_file_icon(filename: str) -> str:
    ext = filename.lower().split(".")[-1] if "." in filename else ""
    mapping = {
        "pdf": "📄",
        "txt": "📝",
        "doc": "📘",
        "docx": "📘",
        "png": "🖼️",
        "jpg": "🖼️",
        "jpeg": "🖼️",
        "mp4": "🎬",
    }
    return mapping.get(ext, "📎")


def format_bytes(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GB"


def validate_file(uploaded_file):
    name = uploaded_file.name
    ext = "." + name.lower().rsplit(".", 1)[-1] if "." in name else ""
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file type: {name}. Allowed: PDF, PNG, JPG, JPEG, MP4, DOC, DOCX, TXT."

    if uploaded_file.size > MAX_FILE_SIZE:
        return False, f"File too large: {name}. Maximum allowed size is 100 MB."

    return True, ""


def generate_demo_response(user_message: str, has_attachments: bool = False) -> str:
    """
    Placeholder response logic.
    Replace this function later with a real backend call.
    """
    return (
        "This is a demo response. Connect the FastAPI backend to enable real AI answers."
    )


# =========================
# Session state setup
# =========================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "pending_files" not in st.session_state:
    st.session_state.pending_files = []

if "upload_error" not in st.session_state:
    st.session_state.upload_error = ""

if "draft_message" not in st.session_state:
    st.session_state.draft_message = ""

# Create an initial conversation if needed
if st.session_state.current_chat_id is None:
    default_chat = make_new_chat()
    st.session_state.current_chat_id = default_chat["id"]
    st.session_state.conversations[default_chat["id"]] = default_chat

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Sovereign AI</div>', unsafe_allow_html=True)

    if st.button("➕ New Chat", key="new_chat_btn", use_container_width=True):
        new_chat = make_new_chat()
        st.session_state.current_chat_id = new_chat["id"]
        st.session_state.conversations[new_chat["id"]] = new_chat
        st.session_state.pending_files = []
        st.session_state.upload_error = ""
        st.session_state.draft_message = ""
        st.rerun()

    st.markdown('<div class="sidebar-label">Recent chats</div>', unsafe_allow_html=True)

    conversations = sorted(
        st.session_state.conversations.values(),
        key=lambda x: x.get("created_at", ""),
        reverse=True,
    )

    if not conversations:
        st.markdown('<div class="small-muted">No chats yet.</div>', unsafe_allow_html=True)
    else:
        for conversation in conversations[:10]:
            conv_id = conversation["id"]
            title = conversation["title"] or "New chat"

            if st.button(
                title,
                key=f"chat_{conv_id}",
                use_container_width=True,
            ):
                st.session_state.current_chat_id = conv_id
                st.session_state.pending_files = []
                st.session_state.upload_error = ""
                st.session_state.draft_message = ""
                st.rerun()

    st.markdown('<div class="sidebar-label">Settings</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear Current Chat", key="clear_chat_btn", use_container_width=True):
        current_id = st.session_state.current_chat_id
        if current_id in st.session_state.conversations:
            st.session_state.conversations[current_id]["messages"] = []
            st.session_state.conversations[current_id]["title"] = "New chat"
        st.session_state.pending_files = []
        st.session_state.upload_error = ""
        st.session_state.draft_message = ""
        st.rerun()

    st.markdown(
        """
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #1f2937; color: #9ca3af; font-size: 0.8rem; text-align: center;">
            <div><strong>Sovereign AI Assistant</strong></div>
            <div style="margin-top: 0.3rem;">Frontend Demo</div>
            <div style="margin-top: 0.2rem;">Backend pending</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# Main chat area
# =========================
current_chat = st.session_state.conversations[st.session_state.current_chat_id]
messages = current_chat.get("messages", [])

st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

# Messages area
st.markdown('<div class="message-area">', unsafe_allow_html=True)

if not messages:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-logo">Sovereign AI Assistant</div>
            <div class="empty-title">How can I help you today?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for message in messages:
        role = message["role"]
        content = message["content"]
        attachments = message.get("attachments", [])

        if role == "user":
            st.markdown('<div class="message-row user-row">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="bubble user-bubble">{content}</div>',
                unsafe_allow_html=True,
            )

            if attachments:
                badge_html = ""
                for file_name in attachments:
                    badge_html += f'<span class="attachment-badge">📎 {file_name}</span>'
                st.markdown(f'<div class="attachment-list">{badge_html}</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown('<div class="message-row assistant-row">', unsafe_allow_html=True)
            st.markdown('<div class="bubble assistant-bubble">', unsafe_allow_html=True)
            st.markdown('<div class="demo-banner">Demo Response</div>', unsafe_allow_html=True)
            st.markdown(content, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Upload section
# =========================
st.markdown('<div class="composer">', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "png", "jpg", "jpeg", "mp4", "doc", "docx", "txt"],
    accept_multiple_files=True,
    help="PDF, PNG, JPG, JPEG, MP4, DOC, DOCX, TXT up to 100 MB each",
    key="uploader",
)

if uploaded_files:
    valid_files = []
    invalid_files = []

    for uploaded_file in uploaded_files:
        ok, error = validate_file(uploaded_file)
        if ok:
            valid_files.append(uploaded_file)
        else:
            invalid_files.append((uploaded_file.name, error))

    if invalid_files:
        st.session_state.upload_error = invalid_files[0][1]
    else:
        st.session_state.upload_error = ""
        st.session_state.pending_files = valid_files

    if st.session_state.pending_files:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        st.markdown('<div class="upload-title">Selected files</div>', unsafe_allow_html=True)
        st.markdown('<div class="upload-helper">Files are displayed before submission and can be removed.</div>', unsafe_allow_html=True)

        for index, file_obj in enumerate(st.session_state.pending_files):
            file_name = file_obj.name
            file_size = format_bytes(file_obj.size)
            file_icon = get_file_icon(file_name)

            col_meta, col_remove = st.columns([0.9, 0.1])

            with col_meta:
                st.markdown(
                    f"""
                    <div class="file-row">
                        <div class="file-meta">
                            <span>{file_icon}</span>
                            <span class="file-name">{file_name}</span>
                            <span class="small-muted">({file_size})</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_remove:
                if st.button("✕", key=f"remove_file_{index}", help=f"Remove {file_name}"):
                    current_files = list(st.session_state.pending_files)
                    current_files.pop(index)
                    st.session_state.pending_files = current_files
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # If the user has cleared files, keep empty selection
    st.session_state.pending_files = []

if st.session_state.upload_error:
    st.markdown(f'<div class="error-banner">❌ {st.session_state.upload_error}</div>', unsafe_allow_html=True)

# Compose message
with st.form("chat_form", clear_on_submit=True):
    st.markdown('<div class="composer-box">', unsafe_allow_html=True)
    user_text = st.text_input(
        "Message Sovereign AI...",
        value=st.session_state.draft_message,
        placeholder="Message Sovereign AI...",
        label_visibility="collapsed",
        key="chat_input",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("➤", use_container_width=False, help="Send message")
    st.session_state.draft_message = user_text

    if submitted:
        clean_text = user_text.strip()

        if clean_text == "":
            st.warning("Please enter a message before sending.")
        else:
            current_chat = st.session_state.conversations[st.session_state.current_chat_id]

            if not current_chat.get("messages"):
                current_chat["title"] = clean_text[:40] + ("..." if len(clean_text) > 40 else "")

            attachments = [f.name for f in st.session_state.pending_files]

            user_message = {
                "role": "user",
                "content": clean_text,
                "attachments": attachments,
            }

            current_chat["messages"].append(user_message)

            with st.spinner("🤖 Sovereign AI is thinking..."):
                time.sleep(0.7)
                assistant_reply = generate_demo_response(clean_text, bool(attachments))

            current_chat["messages"].append({
                "role": "assistant",
                "content": assistant_reply,
            })

            # Save state after send
            st.session_state.pending_files = []
            st.session_state.upload_error = ""
            st.session_state.draft_message = ""
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# End of app
