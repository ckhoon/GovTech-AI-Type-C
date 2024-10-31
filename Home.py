import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Temasek Poly Assistant",
    layout="wide",
)

# Set the correct password
correct_password = "123!@#"

# Initialize session state to track if the password is correct
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Password input and check
if not st.session_state.authenticated:
    st.write("# Access Restricted")
    password = st.text_input("Enter Password", type="password")
    if password == correct_password:
        st.session_state.authenticated = True
        st.success("Access granted! Welcome to the Temasek Polytechnic Assistant.")
        st.rerun()
    elif password:
        st.error("Incorrect password. Please try again.")
        
# Display the main content and sidebar only if authenticated
if st.session_state.authenticated:
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

    # Display disclaimer in an expandable section
    with st.expander("IMPORTANT NOTICE"):
        st.write("""
        This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

        Always consult with qualified professionals for accurate and personalized advice.
        """)
else:
    # If not authenticated, hide sidebar to prevent access to other pages
    st.write("Please enter the correct password to view the available features.")
