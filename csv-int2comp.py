import streamlit as st
import pandas as pd
import requests
import json
import os

st.title("CSV Data Analyzer with Mistral AI")

# Folder path is hardcoded
folder_path = '/Users/connor/dev/hackArizona/Biosphere-Ocean-Data'

# Function to send data to Ollama
def query_mistral(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        response_json = response.json()
        if 'response' in response_json:
            return response_json['response']
        else:
            raise ValueError(f"Invalid response from Mistral API: 'response' key not found. Full response: {response_json}")
    except Exception as e:
        return f"Error querying Mistral API: {str(e)}"

# Process files when folder is provided
if folder_path:
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not csv_files:
        st.warning("No CSV files found in the selected folder.")
    else:
        combined_info = []
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            st.success(f"File '{csv_file}' successfully found!")
            
            # Read the CSV file using pandas
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                st.error(f"Error reading '{csv_file}': {str(e)}")
                continue
            
            # Display file preview
            st.subheader(f"Data Preview: {csv_file}")
            st.write(df.head())
            
            # Display basic statistics
            st.subheader(f"Basic Statistics: {csv_file}")
            st.markdown(f"**Shape**: {df.shape[0]} rows, {df.shape[1]} columns")
            st.markdown(f"**Columns**: {', '.join(df.columns.tolist())}")
            
            # Display summary statistics
            try:
                st.markdown("**Summary Statistics:**")
                st.write(df.describe())
            except Exception as e:
                st.error(f"Error generating summary statistics for '{csv_file}': {str(e)}")
            
            # Information about the dataset to send to the model
            info = {
                "filename": csv_file,
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "data_types": {str(k): str(v) for k, v in df.dtypes.items()},
                "head": df.head().to_dict(orient="records"),
                "describe": df.describe().to_dict()
            }
            combined_info.append(info)
        
        # Convert combined information to a string representation for the AI
        combined_prompt = "Analyze the following CSV data and provide insights:\n\n"
        for info in combined_info:
            combined_prompt += f"""
            Filename: {info['filename']}
            Number of rows: {info['shape'][0]}
            Number of columns: {info['shape'][1]}
            
            Column names: {', '.join(info['columns'])}
            
            Data types:
            {json.dumps(info['data_types'], indent=2)}
            
            Sample data (first 5 rows):
            {json.dumps(info['head'], indent=2)}
            
            Statistical summary:
            {json.dumps(info['describe'], indent=2)}
            
            """
        combined_prompt += """
        Please provide:
        1. A brief overview of what these datasets contain
        2. Key observations about the data
        3. Potential patterns or trends you notice
        4. Suggestions for further analysis or visualization
        5. Any data quality issues that should be addressed
        """
        
        # Show a spinner while waiting for the AI response
        with st.spinner("Analyzing data from all CSV files with Mistral AI..."):
            try:
                analysis = query_mistral(combined_prompt)
                
                # Display the AI analysis
                st.subheader("AI Analysis: Combined CSV Files")
                st.markdown(analysis)
                
            except Exception as e:
                st.error(f"Error querying Mistral AI: {str(e)}")
                st.info("Make sure Ollama is running with the Mistral model loaded. Run 'ollama run mistral' in your terminal.")
else:
    st.info("Please enter the path to the folder containing CSV files to begin analysis.")