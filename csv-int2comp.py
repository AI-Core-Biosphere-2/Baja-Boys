import streamlit as st
import pandas as pd
import requests
import json
import os

st.title("Biosphere 2 Acquired Data Analysis")

# Initialize session state for chat history and data
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = {}

# Hardcoded folder path (modify as needed)
folder_path = '/Users/connor/dev/hackArizona/Biosphere-Ocean-Data'

def query_mistral(prompt, context):
    system_prompt = f"""
    You're a data analyst AI working with these datasets:
    {context}
    
    Guidelines:
    1. Answer questions based on the provided data
    2. Reference specific columns and datasets when relevant
    3. Highlight interesting patterns
    4. Note data quality issues
    5. Suggest visualizations where appropriate
    6. Be concise but informative
    """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }
        )
        return response.json().get('response', 'No response found')
    except Exception as e:
        return f"Error: {str(e)}"

def create_data_context():
    context = []
    for filename, df in st.session_state.loaded_data.items():
        context.append(f"""
        Dataset: {filename}
        - Columns: {', '.join(df.columns)}
        - Row count: {len(df)}
        - Sample values: {df.head(3).to_string(index=False)}
        """)
    return "\n".join(context)

# Load CSV files on initial run
if not st.session_state.loaded_data and folder_path:
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    for csv_file in csv_files:
        try:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path)
            st.session_state.loaded_data[csv_file] = df
        except Exception as e:
            pass  # Silently skip files with errors instead of showing them

# Display chat interface
if st.session_state.loaded_data:
    st.subheader("Chat with Your Data")
    
    # Display chat history
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
    
    # Get user question
    if prompt := st.chat_input("Ask about the data..."):
        # Add user question to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Create data context for the question
        context = create_data_context()
        
        # Generate response
        with st.spinner("Thinking hard..."):
            response = query_mistral(
                f"User question: {prompt}\n\nContext: {context}",
                context
            )
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to update display
        st.rerun()
else:
    st.info("Loading data... Please wait" if folder_path else "No folder path configured")
