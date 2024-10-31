import streamlit as st

if not st.session_state.authenticated:
    st.info('Please Login from the Home page and try again.')
    st.stop()

st.title("About Us ℹ️")

st.markdown("""
## Project Scope
This application serves as an intelligent assistant for Temasek Polytechnic,
helping both adult learners and industrial partners.

## Objectives
- 1. Assist adult learners in finding suitable CET courses
- 2. Guide industrial partners in exploring collaboration opportunities

## Data Sources
- Temasek Polytechnic website
- Obtain via Web crawl script webScaper.py
- Libraries used
    - BeautifulSoup
    - RobotFileParser

## Key Features
1. **Intelligent Query Classification**
   - Automatically determines whether you're interested in courses or partnerships
   - Provides targeted responses based on your needs

2. **Natural Conversation**
   - Easy-to-use chat interface
   - Context-aware responses
""")
