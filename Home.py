import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Temasek Poly Assistant",
    layout="wide"
)

st.title("Welcome to Temasek Polytechnic Assistant")
st.markdown("""
This intelligent assistant helps both adult learners and industry partners connect with Temasek Polytechnic.

### 🎯 What can you do here?

1. **Chat Assistant** 💬
   - Get personalized CET course recommendations
   - Learn about industry collaboration opportunities
   
2. **About Us** ℹ️
   - The project scope, objectives, data sources, and features.
   
3. **Methodology** 📚
   - Data flows and implementation details

### Select a page from the sidebar to get started!
""")