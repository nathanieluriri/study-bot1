import streamlit as st
import time
from pathlib import Path
from langchain_openai import ChatOpenAI
from extraction import extract_text_from,Get_chunks
from variables import Get_questions,Get_Notes

llm = ChatOpenAI(temperature=1,model="gpt-3.5-turbo-1106")
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)








def run_once():
    if "user_info" not in st.session_state:
        st.session_state.user_info = False


    if "signed_in" not in st.session_state:
        st.session_state.signed_in = False

    if "t2" and "t1" and "t3" not in st.session_state:
        st.session_state.t1 = False
        st.session_state.t2 = False
        st.session_state.t3 = False
    if "disabled" not in st.session_state:
        st.session_state.disabled = False


    if "Prompt" not in st.session_state:
        st.session_state.Prompt = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if 'note' not in st.session_state:
        
        st.session_state.note= {'status':"Upload a note to experience AI Magic. If not uploaded yet, create one to explore the magic.",'content':None}

    if "text_content" not in st.session_state:
        st.session_state.text_content =None
    if "Question_with_context" not in st.session_state:

        st.session_state.Question_with_context = {}
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "AInote" not in st.session_state:
        st.session_state.AInote = []
        

st.set_page_config("Study with Botly 🤖",page_icon=":books:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_link__qRIco{display:None;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def check(look_for,lst):
    for checkme in lst:
        if look_for.strip() in checkme.strip():
            return f"{checkme}"
    return False

def look(look_for,dct):
    for checking in dct:
        for check in checking:
            if look_for in checking[check]:
                return checking
        
        
def get_key_and_value(dictionary, key):
    if key in dictionary:
        return key, dictionary[key]
    else:
        return None, None

def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None
def response_calculator(Prompt):
    if Prompt:
        
        it_is_there=check(Prompt,st.session_state.questions)
        
        
        if it_is_there != False:
            ContextwQuestion =look(it_is_there,st.session_state.Question_with_context)
            key = get_key_by_value(ContextwQuestion, it_is_there)
            
            context, Question = key,it_is_there

            
            sysm="You're adept at providing answers and insights to questions given to be analyzed. You use the context provided below as a guide so make sure you don't use your training knowledge unless its to make things easier to understand . Your goal is to offer clear, concise answers that illuminate the essence of the content presented."
            messages = [
            SystemMessage(content=sysm)
            ]

            messages.append(HumanMessage(content=f"Answer these Questions</Question>{Question}<Question/> and use this context for reference</context/>{context}</context/> provide clear and easy to follow explanations using simple grammar"))
            Ai_message = llm(messages)        
            
            Ai_response = Ai_message.content

            return Ai_response


    
    return f"I am only here to respnd to questions from your note and You haven't uploaded a note yet {st.session_state.user_info['given_name']}"


def user(Prompt):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    user_prompt = st.chat_message("user")
    user_prompt.write(Prompt)
    print(Prompt)
    st.session_state.messages.append({"role":"user","content":Prompt})
    return True

def bot_response(Prompt):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    bot_res = st.chat_message("assistant")
    The_gist = response_calculator(Prompt)
    
    bot_res.write(The_gist)
    st.session_state.messages.append({ "role":"assistant", "content":The_gist})

def display_previous_chats ():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    

with st.sidebar:
    run_once()


    if st.session_state.signed_in == False:

        user_info = {'given_name':'Gabriel'}      # login_button(clientId = clientId, domain = domainName, key="login")

        st.session_state.user_info = user_info

        if user_info != False:

            st.session_state.signed_in = True

        elif user_info == False:

            st.session_state.signed_in = False


    


auth_state = None

# write logic for a logout 



def main_ui():

    st.info("Use the test questions generated for quick answers from Botly. Check notes if needed. The function would be made available once the notes are generated", icon="✔")

    with st.sidebar:
        st.success(f" Welcome Back {st.session_state.user_info['given_name']}")

        if st.button("[TO Start a new session] ", type='primary'):
            st.markdown("[Click me ](/)")

    History_Tab, AI_Note, Practice_test, Botly_replies = st.tabs(["Recently generated Notes", "AI Personalized Note", "Practice Test", "Botly replies"])

    with History_Tab:  # History  tab
        with st.container(border=True):
            st.session_state.note['content'] = st.file_uploader("Upload PDF's", type=["Pdf", "Pptx", "docx"],
                                                               help="Upload PDFs or slides or word documents to generate a personalized note",
                                                               disabled=st.session_state.disabled)

        if st.button("Create my note"):
            st.session_state.note['status'] = 'In Progress'
            st.session_state.text_content = extract_text_from(st.session_state.note['content'])

            if st.session_state.text_content is not None:
                st.session_state.note['status'] = 'In Progress'
                st.session_state.chunks = Get_chunks(st.session_state.text_content)
                st.session_state.questions, st.session_state.Question_with_context = Get_questions(
                    st.session_state.chunks)

    with AI_Note:
        if st.session_state.note['status'] != 'ready':  # in case the note isn't ready, it should display something

            if st.session_state.note['status'] == 'In Progress':
                st.info(f"CURRENT STATE : {st.session_state.note['status']}", icon="🔥")
                st.session_state.AInote, st.session_state.note['status'] = Get_Notes(st.session_state.chunks)
                st.write(f" Your Note Is {st.session_state.note['status']} Click the Button below to view it")
                st.button("click me ! ")

            elif st.session_state.note['status'] != 'In Progress':
                st.error(f"CURRENT STATE : {st.session_state.note['status']}", icon="🚨")

        elif st.session_state.note['status'] == 'ready':
            st.success(f" {st.session_state.note['status']}", icon="🎁")
            for noted in st.session_state.AInote:  # Ai Note is a list
                st.markdown(noted)

    with Practice_test:
        st.session_state.chapter_count = "2"
        with st.container(border=True):
            st.markdown("##### ~Greetings, everyone!~ Greetings Gabriel `How` are `you` `doing`? `Are` `you` `ready` `for` `the` `test`? `If` `you` `can` `confidently` `answer` `all` `the` `questions`, know that `you` `are` `prepared` `for` `anything`. Best of luck! ")

        if st.session_state.questions:
            for question in st.session_state.questions:
                st.code(f" [SECTION] {st.session_state.questions.index(question) + 1}")
                st.markdown(question)

    st.session_state.user_inquiry = st.chat_input("Paste the test questions here to receive concise answers from my notes.")

    with Botly_replies:
        display_previous_chats()
        if st.session_state.user_inquiry:
            success = user(st.session_state.user_inquiry)
            if success:
                bot_response(st.session_state.user_inquiry)




































if st.session_state.user_info != False:
    auth_state = True
    pk_status = True   # check_if_pk_exists(PK=st.session_state.user_info["sub"],YourTableName="Users",yourPrimaryKeyColumn="UserID")

    if pk_status == True: # after first time logging in
        
        profile_completeness= True  # fk_status_profile_completeness(st.session_state.user_info['sub'])
        if profile_completeness ==True:
            main_ui()
            

                    
                    
    

                    
                    


        else: # Complete profile 
            pass

























if st.session_state.user_info == False:
    auth_state = False


        


