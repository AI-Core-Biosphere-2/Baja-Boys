import streamlit as st
import pandas as pd
import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

st.title("CSV Data Chat Analyst")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'loaded_data' not in st.session_state:
    st.session_state.loaded_data = {}

def handle_error(message, user_facing=False):
    """Log errors internally and show user-friendly messages when needed"""
    logging.error(message)
    if user_facing:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Sorry, I encountered an issue processing that request. Please try again."
        })

def safe_read_csv(file_path):
    """Read CSV with error handling"""
    try:
        return pd.read_csv(file_path, engine='python')
    except Exception as e:
        handle_error(f"CSV read error for {file_path}: {str(e)}")
        return None

def query_mistral(prompt, context):
    """Query Mistral with error suppression"""
    system_prompt = f"""
    You're analyzing these datasets:
    {context}
    Guidelines: Be accurate, cite specific data, note issues.
    """
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "system": system_prompt},
            timeout=30
        )
        return response.json().get('response', "I couldn't process that request. Please try rephrasing.")
    except Exception as e:
        handle_error(f"Mistral API error: {str(e)}")
        return "The analysis service is currently unavailable. Please try again later."

# Hardcoded folder path
folder_path = '/Users/connor/dev/hackArizona/Biosphere-Ocean-Data'

# Silent data loading
if not st.session_state.loaded_data and os.path.exists(folder_path):
    try:
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            df = safe_read_csv(file_path)
            if df is not None:
                st.session_state.loaded_data[csv_file] = df
    except Exception as e:
        handle_error(f"Folder loading error: {str(e)}")

# Chat interface
if st.session_state.loaded_data:
    st.subheader("Ask About the Data")
    
    # Display chat history
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])
    
    # Handle user input
    if prompt := st.chat_input("Type your question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        try:
            context = "\n".join([
                f"Dataset {name}: Columns {', '.join(df.columns)}, {len(df)} rows"
                for name, df in st.session_state.loaded_data.items()
            ])
            
            response = query_mistral(prompt, context)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
        except Exception as e:
            handle_error(f"Chat processing error: {str(e)}", user_facing=True)
        
        st.rerun()

elif folder_path:
    st.info("No valid CSV files found in the specified folder.")

# Data preview section
if st.session_state.loaded_data:
    with st.expander("View Dataset Previews", expanded=False):
        for name, df in st.session_state.loaded_data.items():
            st.write(f"**{name}** (showing first 3 rows)")
            st.dataframe(df.head(3))
