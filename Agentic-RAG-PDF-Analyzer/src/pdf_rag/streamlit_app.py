import streamlit as st
import os
from pathlib import Path
from crew import PdfRag
import tempfile
import shutil

# Set page config
st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def save_uploaded_file(uploaded_file):
    """Save uploaded file to input_pdf directory"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    pdf_dir = project_root / "input_pdf"
    pdf_dir.mkdir(exist_ok=True)
    
    file_path = pdf_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

def main():
    st.title("📚 PDF Question Answering System")
    
    # Sidebar
    with st.sidebar:
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file:
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"File uploaded successfully!")
            
            # Display PDF info
            st.header("PDF Information")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"Size: {uploaded_file.size/1024:.2f} KB")

    # Main content area
    if uploaded_file:
        # Question input
        st.header("Ask a Question")
        question = st.text_input("Enter your question about the PDF content:")
        
        if st.button("Get Answer"):
            if question:
                with st.spinner("Processing your question..."):
                    try:
                        # Initialize PdfRag and get answer
                        result = PdfRag().crew().kickoff(inputs={
                            'input': question,
                            'pdf_name': uploaded_file.name
                        })
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'question': question,
                            'answer': result
                        })
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        
        # Display chat history
        if st.session_state.chat_history:
            st.header("Chat History")
            # Reverse the chat history to show newest first
            for chat in reversed(st.session_state.chat_history):
                with st.container():
                    st.subheader(f"Q: {chat['question']}")
                    st.markdown(chat['answer'])
                    st.divider()
    else:
        st.info("Please upload a PDF file to begin.")

if __name__ == "__main__":
    main()