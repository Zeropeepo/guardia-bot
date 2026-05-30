import streamlit as st
import requests

API_URL = "http://localhost:8000/api/chat"

st.set_page_config(page_title="Guardia Bot", layout="wide")
st.title("Guardia Bot 🛡️")
st.markdown("Your educational cybersecurity tutor.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar filters
st.sidebar.header("Filters")
topic_filter = st.sidebar.text_input("Topic", "")
level_filter = st.sidebar.selectbox("Level", ["", "beginner", "intermediate", "advanced"])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("Sources"):
                for idx, src in enumerate(msg["sources"]):
                    st.markdown(f"**[{idx+1}] {src.get('document_title', 'Unknown')}** (Score: {src.get('relevance_score', 0):.2f})")
                    st.text(src.get('text', ''))

if prompt := st.chat_input("Ask about cybersecurity..."):
    # Append user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Call API
    payload = {
        "question": prompt,
        "topic_filter": topic_filter if topic_filter else None,
        "level_filter": level_filter if level_filter else None
    }
    
    try:
        with st.spinner("Thinking..."):
            resp = requests.post(API_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            
            answer = data["answer"]
            sources = data.get("sources", [])
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "sources": sources
            })
            
            with st.chat_message("assistant"):
                st.write(answer)
                if sources:
                    with st.expander("Sources"):
                        for idx, src in enumerate(sources):
                            st.markdown(f"**[{idx+1}] {src.get('document_title', 'Unknown')}** (Score: {src.get('relevance_score', 0):.2f})")
                            st.text(src.get('text', ''))
                st.caption(f"Latency: {data.get('latency_ms', 0):.2f} ms")
                
    except Exception as e:
        st.error(f"Error communicating with backend: {e}")
