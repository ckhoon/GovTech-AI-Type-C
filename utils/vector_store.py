import os
from pathlib import Path
from typing import List, Dict
import json
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def load_json_files(directory_path: str) -> List[Dict]:
    """Load multiple JSON files from a directory with error handling"""
    json_files = []
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        st.error(f"Directory not found: {directory_path}")
        return json_files
    
    # List all files in directory
    files = list(Path(directory_path).glob('*.json'))
    if not files:
        st.warning(f"No JSON files found in {directory_path}")
        return json_files
    
    # Process each file
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                st.info(f"Processing file: {file_path}")
                data = json.load(file)
                if not data.get('content'):
                    st.warning(f"No content found in {file_path}")
                    continue
                    
                processed_text = f"URL: {data.get('url', 'No URL')}\n"
                processed_text += f"Title: {data.get('title', 'No Title')}\n"
                processed_text += f"Content: {data.get('content', 'No Content')}"
                
                if len(processed_text.strip()) > 0:
                    json_files.append(processed_text)
                else:
                    st.warning(f"Processed text is empty for {file_path}")
                
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON from {file_path}: {str(e)}")
        except Exception as e:
            st.error(f"Error processing {file_path}: {str(e)}")
    
    return json_files

def initialize_vectorstore():
    """Initialize Chroma vectorstore with document data if it doesn't exist"""
    persist_directory = "chroma_db"
    
    # Check for existing vector store
    if os.path.exists(persist_directory):
        try:
            embeddings = OpenAIEmbeddings()
            vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            st.success("Successfully loaded existing vector store")
            return vector_store
        except Exception as e:
            st.error(f"Error loading existing vector store: {str(e)}")
            # If loading fails, we'll recreate the vector store
            import shutil
            shutil.rmtree(persist_directory, ignore_errors=True)
    
    # Load data from both directories
    st.info("Loading CET course data...")
    cet_data = load_json_files("data/cet_courses")
    st.info(f"Loaded {len(cet_data)} CET course documents")
    
    st.info("Loading partnership data...")
    partnership_data = load_json_files("data/partnerships")
    st.info(f"Loaded {len(partnership_data)} partnership documents")
    
    all_texts = cet_data + partnership_data
    
    if not all_texts:
        st.error("No valid documents found to create vector store")
        raise ValueError("No documents available for vector store creation")
    
    # Split texts
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    texts = []
    for text in all_texts:
        chunks = text_splitter.split_text(text)
        texts.extend(chunks)
        
    st.info(f"Created {len(texts)} text chunks for indexing")
    
    if not texts:
        st.error("No text chunks created after splitting")
        raise ValueError("Text splitting resulted in no chunks")
    
    try:
        # Create vector store
        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        st.success("Successfully created and persisted new vector store")
        return vector_store
        
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        raise