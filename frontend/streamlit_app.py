import streamlit as st
import requests
import os

# Streamlit page setup
st.set_page_config(
    page_title="Secure Chat Guardian",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# App Title & Subtitle with Modern Styling
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ Secure Chat Guardian</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-size: 1.1em;'>A secure client-server Assistant powered by Groq LLaMA & FAISS RAG</p>", unsafe_allow_html=True)
st.markdown("---")

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Check backend status
backend_healthy = False
try:
    health_check = requests.get(BACKEND_URL, timeout=2)
    if health_check.status_code == 200:
        backend_healthy = True
except Exception:
    backend_healthy = False

# Sidebar Configuration
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    
    # Connection status indicator
    if backend_healthy:
        st.success("🟢 Connected to Backend Server")
    else:
        st.error("🔴 Backend Server Offline")
        st.info("💡 Run the backend server using:\n`python3 -m uvicorn backend.main:app --reload`")
        
    # Chat mode selection
    chat_mode = st.radio(
        "💬 Choose Chat Mode",
        options=["General Mode", "PDF Document Mode (RAG)"],
        index=0,
        help="General Mode chats directly with LLaMA. PDF Document Mode queries LLaMA with context fetched from simple.pdf."
    )
    
    st.markdown("---")
    
    # PDF Document Upload
    st.markdown("### 📤 Upload PDF Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file to index:",
        type=["pdf"],
        help="Upload a new document to extract text and register it in the vector store.",
        disabled=not backend_healthy
    )
    
    # Initialize tracking of processed files (both successes and failures) to avoid infinite loops on reruns
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    
    if uploaded_file is not None:
        if uploaded_file.name not in st.session_state.processed_files:
            st.session_state.processed_files.add(uploaded_file.name)
            with st.spinner(f"Indexing '{uploaded_file.name}'..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{BACKEND_URL}/api/upload", files=files, timeout=60)
                    if response.status_code == 200:
                        st.success(f"✅ Indexed {uploaded_file.name} successfully!")
                    else:
                        error_detail = response.json().get("detail", response.text)
                        st.error(f"❌ Upload failed: {error_detail}")
                except Exception as e:
                    st.error(f"🔌 Connection failed: {e}")
    else:
        # Clear tracker when uploader is cleared, allowing retry
        st.session_state.processed_files = set()
                    
    st.markdown("---")
    
    # Actions
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous conversation messages
for chat in st.session_state.chat_history:
    with st.chat_message("user" if chat["role"] == "user" else "assistant"):
        st.markdown(chat["content"])
        if "sources" in chat and chat["sources"]:
            with st.expander("📚 View Document Context Used"):
                for idx, src in enumerate(chat["sources"]):
                    st.markdown(f"**Source {idx+1}:** {src}")

# Chat input from user
user_input = st.chat_input("Type your message here...", disabled=not backend_healthy)

if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Re-display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Fetch response from backend
    with st.spinner("🤖 Guardian is thinking..."):
        try:
            if chat_mode == "PDF Document Mode (RAG)":
                endpoint = f"{BACKEND_URL}/api/chat_with_pdf"
            else:
                endpoint = f"{BACKEND_URL}/api/generate"
                
            response = requests.post(
                endpoint,
                json={"message": user_input},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get("reply", "No response content received.")
                sources = result.get("sources", [])
                
                # Append assistant reply to session state
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": reply,
                    "sources": sources
                })
                
                # Render the assistant response
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    if sources:
                        with st.expander("📚 View Document Context Used"):
                            for idx, src in enumerate(sources):
                                st.markdown(f"**Source {idx+1}:** {src}")
            else:
                error_detail = response.json().get("detail", response.text)
                st.error(f"Backend Server Error: {error_detail}")
                
        except requests.exceptions.Timeout:
            st.error("⏳ Request timed out. The backend server took too long to reply.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection error. Lost contact with the backend server.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")