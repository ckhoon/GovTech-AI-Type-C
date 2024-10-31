import streamlit as st
from streamlit_mermaid import st_mermaid

st.title("Methodology 📚")
st.markdown("""
## Technical Implementation
### 1. Data Collection and Processing
- Web crawling of Temasek Polytechnic website
- Processing of multiple JSON files
- Text chunking for optimal retrieval
### 2. Vector Store Implementation
- Using Chroma for persistent vector storage
- Efficient document retrieval
- Automatic embeddings updates
### 3. Intent Classification
- CrewAI-powered query analysis
- Automatic classification of user intentions
- Adaptive response generation
### 4. RAG (Retrieval Augmented Generation)
- Context-aware response generation
- Integration with LangChain
- Custom prompting based on query type
### 5. User Interface
- Streamlit-based web application
- Multi-page organization
- Persistent chat history
""")

# Use st_mermaid instead of markdown for the diagram
st_mermaid("""
graph TD
    A[User Query] --> B[Intent Classification]
    B --> C{Query Type}
    C -->|Adult Learner| D[CET Course RAG]
    C -->|Industry Partner| E[Partnership RAG]
    D --> F[Response Generation]
    E --> F
    F --> G[User Interface]
""", height=600)