# Sovereign AI Assistant

A standalone ChatGPT-inspired Streamlit frontend for a college mini project. This version works independently without a backend and uses placeholder responses so your team can connect a real FastAPI backend later.

## Features

- Dark ChatGPT-style interface
- Left sidebar with:
  - New Chat button
  - Recent chat history
  - Clear chat option
- Conversational user/assistant layout
- Welcome message: "How can I help you today?"
- Text input with placeholder: "Message Sovereign AI..."
- Send button with arrow icon
- Loading spinner
- Empty state for new conversations
- Multi-file upload support:
  - PDF
  - PNG
  - JPG
  - JPEG
  - MP4
  - DOC
  - DOCX
  - TXT
- File validation and support for removing files before sending
- Demo response mode with clear explanation that backend integration is required
- Current browser session conversation persistence

## Project structure

```bash
miniproject/
├── app.py
├── requirements.txt
└── README.md
