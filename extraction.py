import streamlit as st
from pdf_doc import pdf_converter
from word_document import docx_converter
from ppt import ppt_converter
from langchain.text_splitter import CharacterTextSplitter

@st.cache_data(ttl=300,persist="disk")
def extract_text_from(doc):
    if doc != None:
        if "pdf" in doc.name:
            text = pdf_converter(doc)
            

        elif "docx" in doc.name:
            text = docx_converter(doc)
            

        elif "pptx" in doc.name:
            text = ppt_converter(doc)
            
        return text
        
@st.cache_data(ttl=300,persist="disk")
def get_chunks_from_extracted_texts(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunk = text_splitter.split_text(raw_text)
    return chunk
@st.cache_data(ttl=300,persist="disk")
def Get_chunks(extracted_text):
    chunks = get_chunks_from_extracted_texts(extracted_text)
    # st.json(chunks)
    return chunks