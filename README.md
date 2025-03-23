# B2Twin Hackathon Project: Biosphere 2 Digital Twin
## Introduction
Biosphere 2, a research facility dedicated to understanding Earth's intricate and intelligent ecosystems, has inspired our project to create a digital twin using Artificial Intelligence and Machine Learning. Our goal is to innovate ways to restore degraded environments on Earth and prepare for space travel.

## Project Overview
Our project, built using Streamlit and AI models, provides a user-friendly interface that works with the Ocean dataset:

The color of these buttons indicates whether all data is within tolerance for these datasets. The main menu features a chatbot that summarizes the status of the three datasets and refreshes the data periodically.

Each dataset menu includes:
* A chatbox to inquire about different parts of the biosphere
* Summary values and charts to display key information

## Goal
Our ultimate goal is to connect to the comprehensive Biosphere 2 data archive and discover useful scientific and creative applications.

## Requirements
* Python libraries: installed via `https://www.python.org/downloads/`
* Visual Studio Code or similar tool: installed via `https://code.visualstudio.com/`
* Streamlit or similar UI library: installed via `https://streamlit.io/`

## Installation
1. Install the required libraries and tools.
2. Clone the repository: `git clone https://github.com/AI-Core-Biosphere-2/B2Twin-Hackathon.git`
3. Install the AI model using Ollama: `https://ollama.com/`
4. Download the Biosphere 2 sensor data .csv files from GitHub/Google Drive: `https://github.com/AI-Core-Biosphere-2/B2Twin-Hackathon`

## Usage
1. Run the Streamlit app: `streamlit run app.py`
2. Select a dataset from the main menu.
3. Use the chatbox to inquire about different parts of the biosphere.
4. View the summary values and charts to display key information.

## Roadmap
* Stage 1: Get LLM running on local machine
* Stage 2: Grab starter data from GitHub and learn to make them usable by LLM
* Stage 3: Connect to comprehensive data archive for access to all data and do something useful with it
* Stage 4: Get LLMs to talk to each other and work together to do science
