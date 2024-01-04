import streamlit as st 

from langchain_community.chat_models import ChatOpenAI


llm = ChatOpenAI(openai_api_key="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",temperature=1)

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from langchain.memory import ConversationSummaryMemory

















def Get_questions(user_input):
    st.session_state.note['status'] = 'In Progress'
    sysm="You're a question-crafting expert, ready to dissect any text you're given. Uncover its core ideas, evidence, impact, and connections. Ask unique, insightful questions that spark deep understanding. No repeats, just pure essence exploration! ask only a maximum of 3 questions"
    messages = [
    SystemMessage(content=sysm)
]
    AIres_with_context = {}
    AIres = []
    for user in user_input:
        if len(messages) == 3:
            messages.pop(2)
            messages.pop(1)
            counter = 1
        messages.append(HumanMessage(content="{}".format(user)))
        Ai_message = llm(messages)        
        
        Ai_response = Ai_message.content
        messages.append(AIMessage(content="{}".format(Ai_response)))
        AIres.append(Ai_response)
    
        AIres_with_context.update({user:Ai_response})

    
    return AIres,AIres_with_context



def Get_Notes(user_input):
    st.session_state.note['status'] = 'In Progress'
    sysm="You're an AI-powered study partner specializing in note creation. Your mission is to analyze provided text, organize it into coherent sections, and generate concise notes. Use Markdown language for clarity and aesthetics, and highlight key points with :blue[key point]. Your goal is to make the context understandable and create short notes on each section. Ensure that the notes are well-structured, easy to follow, and capture the essence of the given information."
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
        Ai_message = llm(messages)        
        
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

    