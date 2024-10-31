from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def get_custom_prompt(user_type):
    """Get custom prompt based on user type"""
    if user_type == "adult_learner":
        template = """You are a helpful educational advisor for Temasek Polytechnic. Use the following context to answer questions about CET courses for adult learners. Focus on course relevance, prerequisites, and career advancement opportunities. 
        
        Context: {context}
                
        Human: {input}
        Assistant:"""
        
        contextualize_template = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question that can be queried against a vector database. 
        
        Chat History:
        {chat_history}
                
        Human: {input}
        Assistant:"""
        
    elif user_type == "industrial_partner":
        template = """You are a partnership advisor for Temasek Polytechnic. Use the following context to answer questions about collaboration opportunities. Focus on partnership models, benefits, and success stories. 
        
        Context: {context}
                
        Human: {input}
        Assistant:"""
        
        contextualize_template = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question that can be queried against a vector database. 
        
        Chat History:
        {chat_history}
                
        Human: {input}
        Assistant:"""
        
    else:
        template = """You are an assistant for Temasek Polytechnic. Use the following context to answer questions about enquiries about the polytechnic. If the questions are out of the polytechnic context, please reply that you don't know the answer. 
        
        Context: {context}
                
        Human: {input}
        Assistant:"""
        
        contextualize_template = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question that can be queried against a vector database. 
        
        Chat History:
        {chat_history}
                
        Human: {input}
        Assistant:"""
    
    # Create prompts
    question_prompt = PromptTemplate.from_template(template)
    contextualize_prompt = PromptTemplate.from_template(contextualize_template)
    
    return question_prompt, contextualize_prompt

def create_chat_chain(vectorstore, user_type):
    """Create conversation chain with custom prompt and source document tracking"""
    # Initialize LLM
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # Get custom prompts
    question_prompt, contextualize_prompt = get_custom_prompt(user_type)
    
    # Create history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, 
        vectorstore.as_retriever(), 
        contextualize_prompt
    )
    
    # Create document chain
    document_chain = create_stuff_documents_chain(
        llm,
        question_prompt
    )
    
    # Create retrieval chain
    retrieval_chain = create_retrieval_chain(
        history_aware_retriever, 
        document_chain
    )
    
    return retrieval_chain

# Example usage with source document tracking
def process_query(retrieval_chain, query, chat_history):
    """Process a query with the retrieval chain and return sources"""
    result = retrieval_chain.invoke({
        "input": query,
        "chat_history": chat_history
    })
    
    return {
        "answer": result['answer'],
        "source_documents": result.get('context', [])  # Retrieve the context/source documents
    }