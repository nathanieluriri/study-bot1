import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from extraction import extract_text_from,Get_chunks
from variables import Get_questions



if "notes" not in st.session_state:
    st.session_state.notes = None


if "text_content" not in st.session_state:
    st.session_state.text_content =None
if "Question_with_context" not in st.session_state:

    st.session_state.Question_with_context = {}
if "questions" not in st.session_state:
    st.session_state.questions = []


st.session_state.notes = st.file_uploader("enter your note",type=["PDF","pptx","docx"])


st.session_state.text_content = extract_text_from(st.session_state.notes) # extract text from file first
if st.session_state.text_content != None:

    st.session_state.chunks = Get_chunks(st.session_state.text_content) # Get chunks from extracted text

    st.session_state.questions,st.session_state.Question_with_context =Get_questions(st.session_state.chunks)
    # st.json(Question_with_context)
    # st.json(st.session_state.questions)



if st.session_state.questions:
    for question in st.session_state.questions:
        st.markdown(question)



