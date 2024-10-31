import streamlit as st

if not st.session_state.authenticated:
    st.info('Please Login from the Home page and try again.')
    st.stop()

from utils.vector_store import initialize_vectorstore
from utils.intent_classifier import create_intent_classification_crew
from utils.chat_chain import create_chat_chain

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None

st.title("Chat Assistant 💬")

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.user_question = ""


# Initialize vectorstore if not already done
if st.session_state.vector_store is None:
    with st.spinner("Initializing knowledge base..."):
        st.session_state.vector_store = initialize_vectorstore()
        retriever = st.session_state.vector_store.as_retriever()
        test_query = "test query about ENG related CET courses"  # Adjust based on typical queries
        retrieved_docs = retriever.get_relevant_documents(test_query)
        st.write(f"Number of documents retrieved for test query: {len(retrieved_docs)}")

# Initialize intent classifier
classify_intent = create_intent_classification_crew()

# Chat interface
st.subheader("Ask me anything about CET courses or industry partnerships!")


if "user_question" not in st.session_state:
    st.session_state.user_question = ""

def submit():
    st.session_state.user_question = st.session_state.widget
    st.session_state.widget = ""

st.text_input("Your question:", key="widget", on_change=submit)

user_question = st.session_state.user_question

# User input
#user_question = st.text_input("Your question:")

if user_question:
    # Classify user intent
    with st.spinner("Analyzing your question..."):
        user_type = classify_intent(user_question)
        if user_type == 'adult_learner':
            query_type = 'CET Course Query'
        elif user_type == 'industrial_partner':
            query_type = 'Industry Partnership Query'
        else:
            query_type = 'General Query'
        st.info(f"Query classified as: {query_type}")
    
    chain = create_chat_chain(st.session_state.vector_store, user_type)
    
    with st.spinner("Generating response..."):
        response = chain.invoke({
            "input": user_question,
            "chat_history": st.session_state.chat_history
        })
        
        st.session_state.chat_history.append((user_question, response["answer"], response.get('context', [])))

    st.session_state.user_question = ""

# Display chat history
for question, answer , source in st.session_state.chat_history:
    st.write("🙋 You:", question)
    st.write("🤖 Assistant:", answer)
    st.write("---")