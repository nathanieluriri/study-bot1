import streamlit as st 

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=1,api_key=openai_api_key)

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from langchain.memory import ConversationSummaryMemory
















@st.cache_data(ttl=300)
def Get_questions(user_input):
    st.session_state.note['status'] = 'In Progress'
    sysm=f"You're a personalized question-crafting expert, ready to dissect any text you're given specific for a user named {st.session_state.UD.first_name} with a learning rate of {st.session_state.UD.learning_rate}/10 and an understanding rate {st.session_state.UD.understanding_rate}/10. Uncover its core ideas, evidence, impact, and connections. Ask unique, insightful questions that spark deep understanding. No repeats, just pure essence exploration! ask only a maximum of 3 questions and only questions no need to generate short explanations about the essence etc."
    messages = [
    SystemMessage(content=sysm)
]
    AIres_with_context = []
    AIres = []
    for user in user_input:
        if len(messages) == 3:
            messages.pop(2)
            messages.pop(1)
            counter = 1
        messages.append(HumanMessage(content="{}".format(user)))
        Ai_message = llm.invoke(messages)        
        
        Ai_response = Ai_message.content
        messages.append(AIMessage(content="{}".format(Ai_response)))
        AIres.append(Ai_response)
    
        AIres_with_context.append({user:Ai_response})

    
    return AIres,AIres_with_context


@st.cache_data(ttl=300)
def Get_Notes(user_input):
    st.session_state.note['status'] = 'In Progress'
    sysm=f"You're an AI-powered study partner specializing in note creation for a user named {st.session_state.UD.first_name} come up with a good title for your notes make sure not to use [notes for {st.session_state.UD.first_name}] as a title the notes should be for the user who has an understanding rate of {st.session_state.UD.understanding_rate}/10 and a learning rate of approximately {st.session_state.UD.learning_rate}/10 which means keep it to a level it CAN BE UNDERSTOOD THINK OF IT THIS WAY 1= PATRICK STAR IN SPONGEBOB AND 10= EINSTIEN THE FOUNDER OF THE THEORY OF RELATIVITY. Generate concise notes AND make sure to mention the users name in the note 'sometimes' to get attention. Use Markdown language for clarity and aesthetics. Your goal is to make the context understandable for a user with an understanding rate of {st.session_state.UD.understanding_rate}/10 and a learning rate of approximately {st.session_state.UD.learning_rate}/10 . Ensure that the notes are well-structured, easy to follow for {st.session_state.UD.first_name}."
    messages = [
    SystemMessage(content=sysm)
]
    status = "ready"
    AIres = []
    for user in user_input:
        if len(messages) == 3:
            messages.pop(2)
            messages.pop(1)
            counter = 1
        messages.append(HumanMessage(content="provided text:{}".format(user)))
        Ai_message = llm.invoke(messages)        
        
        Ai_response = Ai_message.content
        messages.append(AIMessage(content="{}".format(Ai_response)))
        AIres.append(Ai_response)
    
        

    
    return AIres,status


if "chunks" not in st.session_state:
    st.session_state.chunks = []

Note_creation_prompt="""
Given the provided contextual document, generate Three insightful questions that cover key points, important details, and potential areas for further exploration. These Three questions should help in creating a comprehensive and well-rounded note, capturing the essence of the document and facilitating a deeper understanding of the topic. Consider asking about main ideas, supporting evidence, implications, and any relevant connections or comparisons


</contextual document/>
{}
</contextual document/>

The Three questions generated should be concise and have similar words with the context"""

    