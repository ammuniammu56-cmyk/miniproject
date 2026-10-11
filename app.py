
import streamlit as st

st.set_page_config(
    page_title="Sovereign AI | Automotive Intelligence",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== PREMIUM AUTOMOTIVE THEME ====================
st.markdown("""
<style>
:root {
    --bg: #0A101A;
    --sidebar: #0D1623;
    --panel: #111D2C;
    --panel-hover: #18283A;
    --border: #28394D;
    --teal: #55E6D0;
    --white: #F2F6FC;
    --muted: #9AAEC3;
}

.stApp {
    background: var(--bg);
    color: var(--white);
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label {
    color: var(--white);
}
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}
hr {
    border-color: var(--border);
}
div.stButton > button {
    background: var(--panel);
    color: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
    min-height: 43px;
    transition: 0.2s;
}
div.stButton > button:hover {
    background: var(--panel-hover);
    border-color: var(--teal);
    color: var(--teal);
}
[data-testid="stChatMessage"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 12px;
}
[data-testid="stChatInput"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
}
[data-testid="stChatInput"] textarea {
    color: var(--white);
}
[data-testid="stFileUploader"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 12px;
}
.hero {
    background: linear-gradient(120deg, #14263A, #101925 70%);
    border: 1px solid #30445A;
    border-radius: 22px;
    padding: 32px;
    margin: 18px 0 25px 0;
}
.eyebrow {
    color: var(--teal);
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 2px;
}
.hero h1 {
    font-size: 37px;
    line-height: 1.2;
    margin: 15px 0 12px;
}
.hero p {
    color: #B7C7D9;
    font-size: 15px;
    line-height: 1.8;
}
.card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 18px;
    min-height: 135px;
}
.card-icon {
    font-size: 25px;
}
.card-title {
    color: var(--white);
    font-size: 15px;
    font-weight: 700;
    margin-top: 12px;
}
.card-description {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.6;
    margin-top: 7px;
}
.status-dot {
    color: var(--teal);
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE ====================
if "chats" not in st.session_state:
    st.session_state.chats = {"New conversation": []}

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "New conversation"

if "suggestion" not in st.session_state:
    st.session_state.suggestion = ""

if "pending_files" not in st.session_state:
    st.session_state.pending_files = []


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(
        '<div style="font-size:23px;font-weight:800;">'
        'SOVEREIGN<span style="color:#55E6D0;"> AI</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("AUTOMOTIVE INTELLIGENCE")
    st.divider()

    if st.button("＋  New conversation", use_container_width=True):
        name = f"New conversation {len(st.session_state.chats) + 1}"
        st.session_state.chats[name] = []
        st.session_state.active_chat = name
        st.session_state.pending_files = []
        st.rerun()

    st.markdown("##### WORKSPACE")

    st.markdown("🚘  Vehicle intelligence")
    st.markdown("🏭  Manufacturing knowledge")
    st.markdown("🔧  Service & maintenance")
    st.markdown("📄  Technical documents")

    st.divider()
    st.markdown("##### RECENT CONVERSATIONS")

    for name in list(st.session_state.chats.keys())[::-1]:
        if st.button(
            "◉  " + name,
            key="chat_" + name,
            use_container_width=True,
        ):
            st.session_state.active_chat = name
            st.session_state.pending_files = []
            st.rerun()

    st.divider()
    st.caption("SYSTEM ARCHITECTURE")
    st.caption("Frontend · Streamlit")
    st.caption("Backend · To be connected")
    st.caption("LLM · Ollama planned")


# ==================== TOP BAR ====================
left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="eyebrow">AUTOMOTIVE SYSTEMS / AI WORKSPACE</div>',
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        '<div style="text-align:right;color:#55E6D0;'
        'font-size:12px;">● INTERFACE ONLINE</div>',
        unsafe_allow_html=True,
    )


# ==================== WELCOME DASHBOARD ====================
messages = st.session_state.chats[st.session_state.active_chat]

if not messages:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">ENGINEERING • MANUFACTURING • SERVICE</div>
        <h1>Intelligence that<br>moves the automotive world.</h1>
        <p>
            One workspace for automotive engineering knowledge,
            manufacturing workflows, vehicle servicing and
            technical problem-solving.
        </p>
        <div style="color:#55E6D0;font-size:12px;font-weight:600;">
            PRIVATE-FIRST AI · AUTOMOTIVE KNOWLEDGE WORKSPACE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Explore your workspace")
    st.caption("Choose a task to start a conversation.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🏭</div>
            <div class="card-title">Manufacturing Intelligence</div>
            <div class="card-description">
                Assembly processes, production workflows,
                quality reports and factory maintenance.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore manufacturing  →", use_container_width=True):
            st.session_state.suggestion = (
                "Explain automotive manufacturing workflows, "
                "quality control and production processes."
            )
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🚘</div>
            <div class="card-title">Vehicle Diagnostics</div>
            <div class="card-description">
                Understand diagnostic trouble codes, service
                manuals, vehicle faults and repair information.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore vehicle service  →", use_container_width=True):
            st.session_state.suggestion = (
                "Help me understand vehicle diagnostics, "
                "maintenance and service troubleshooting."
            )
            st.rerun()

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📑</div>
            <div class="card-title">Technical Knowledge</div>
            <div class="card-description">
                Work with service manuals, technical reports
                and engineering documentation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore technical documents  →",
                     use_container_width=True):
            st.session_state.suggestion = (
                "Help me review and summarize an automotive technical manual."
            )
            st.rerun()

    with c4:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🛠️</div>
            <div class="card-title">Quality & Maintenance</div>
            <div class="card-description">
                Examine maintenance records, inspection findings
                and potential manufacturing quality issues.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Explore quality support  →",
                     use_container_width=True):
            st.session_state.suggestion = (
                "Help me analyze an automotive quality inspection "
                "report and identify issues to investigate."
            )
            st.rerun()


# ==================== CONVERSATION HISTORY ====================
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("files"):
            st.caption("📎 " + ", ".join(message["files"]))


# ==================== FILE ATTACHMENTS ====================
with st.expander("＋  Attach manuals, images, videos or reports"):
    uploads = st.file_uploader(
        "Select files for your message",
        type=[
            "pdf", "txt", "md", "csv", "json",
            "png", "jpg", "jpeg", "webp",
            "mp4", "mov", "avi",
            "doc", "docx",
        ],
        accept_multiple_files=True,
        key="automotive_uploads",
    )

    if uploads:
        st.session_state.pending_files = uploads
        for file in uploads:
            st.caption(
                f"📎 {file.name} · {file.size / 1024:.1f} KB"
            )


# ==================== CHAT INPUT ====================
prompt = st.chat_input(
    "Ask about manufacturing, vehicles, maintenance or engineering..."
)

if not prompt and st.session_state.suggestion:
    prompt = st.session_state.suggestion
    st.session_state.suggestion = ""

if prompt:
    filenames = [
        file.name for file in st.session_state.pending_files
    ]

    messages.append({
        "role": "user",
        "content": prompt,
        "files": filenames,
    })

    messages.append({
        "role": "assistant",
        "content": (
            "Your request has been received by the interface.\n\n"
            "**AI connection pending:** This UI is not yet connected "
            "to the language model. Once Ollama, the backend and the "
            "document retrieval pipeline are configured, it can provide "
            "AI-generated responses based on the connected model and "
            "available automotive knowledge sources."
        ),
    })

    if (
        len(messages) == 2
        and st.session_state.active_chat == "New conversation"
    ):
        title = prompt.replace("\n", " ").strip()[:32]
        title = title or "Automotive conversation"

        if title in st.session_state.chats:
            title = f"{title} {len(st.session_state.chats)}"

        st.session_state.chats[title] = (
            st.session_state.chats.pop("New conversation")
        )
        st.session_state.active_chat = title

    st.session_state.pending_files = []
    st.rerun()


# ==================== FOOTER ====================
st.divider()
st.caption(
    "SOVEREIGN AI  ·  AUTOMOTIVE INTELLIGENCE  ·  "
    "DEVELOPMENT INTERFACE"
)
