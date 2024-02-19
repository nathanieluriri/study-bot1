import streamlit as st
import time
from pathlib import Path
from langchain_openai import ChatOpenAI 
from extraction import extract_text_from,Get_chunks
from variables import Get_questions,Get_Notes
from database import history_ID_query, history_query,Chathistory_query,updateChatHistory

llm = ChatOpenAI(temperature=1,model="gpt-3.5-turbo-1106")
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)





from typing import List, Dict, Union
from bson import ObjectId


def title_maping(history_ids:list) ->  List[Dict]:
    """
    This functions maps the users title to history id of a user
    it takes a list of history ID and loops through the id to return 
    the list of titles and history ID objects accordingly
    
    
    """
    Title_map = []
   
    for history_id in history_ids:
        documents = history_query(history_id)
        title = documents[0][0][0].split('\n')[0]
        Title_map.append({"History id":history_id,"Title":title})
    return Title_map



def titles_only(title_map:List[Dict])->List[str]:
    titles = [option['Title'] for option in title_map]
    return titles




def History_id_only(title_map:List[Dict] , selected_title:str)->Union[ObjectId,str]: 
    try:
        selected_history_id = next(option['History id'] for option in title_map if option['Title'] == selected_title)
        
        
    except StopIteration:
        selected_history_id = "Nothing selected"
    return selected_history_id

# # Selectbox returns the selected title directly
# selected_title = st.selectbox(
#     "Select a title",
#     titles,
#     index=None,
#     placeholder="Select a title..."
# )


if "History_IDS" not in st.session_state:
    st.session_state.History_IDS = []

try:
    st.session_state.History_IDS=history_ID_query(st.session_state.UD._id)
except:
    st.switch_page("app.py")

st.session_state.Title_maps = title_maping(st.session_state.History_IDS)
st.session_state.titles = titles_only(st.session_state.Title_maps)

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

    if "Old_messages" not in st.session_state:
        try:
            st.session_state.Old_messages =Chathistory_query(st.session_state.Selected_History_ID)
        except:
            st.session_state.Old_messages =[]

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
            try:
                Ai_message = llm(messages)        
                
                Ai_response = Ai_message.content
            except:
                Ai_response ="You have no network Please try again when there is network"

            return Ai_response


    
    return f"I am only here to respnd to questions from your note and You haven't uploaded a note yet {st.session_state.user_info['given_name']}"


def user(Prompt):

    user_prompt = st.chat_message("user")
    user_prompt.write(Prompt)
    # print(Prompt)
    st.session_state.Old_messages.append({"role":"user","content":Prompt})
    return True

@st.cache_data(ttl=300)
def bot_response(Prompt,_HistoryID):
    bot_res = st.chat_message("assistant")
    The_gist = response_calculator(Prompt)
    
    bot_res.write(The_gist)
    st.session_state.Old_messages.append({ "role":"assistant", "content":The_gist})
    updateChatHistory(ObjectId(_HistoryID),st.session_state.Old_messages)



def display_previous_chats (HistoryID:str):
    st.session_state.Old_messages =Chathistory_query(ObjectId(HistoryID))
    for message in st.session_state.Old_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            

    

with st.sidebar:
    run_once()


    




def main_ui():
    st.markdown('<style> section[data-testid="stSidebar"]{ display: none !important; }</style>', unsafe_allow_html=True)

    History_Tab, AI_Note, Practice_test, Botly_replies = st.tabs(["Recently generated Notes", "AI Personalized Note", "Practice Test", "Botly replies"])

    with History_Tab:  # History  tab
    
        if st.button("Create A New Note",type='primary'):
                        st.switch_page("app.py")

        st.selectbox(
            "Select a History",
            index=None,
            options=st.session_state.titles,
            placeholder="Select a History you want to return to...",
            key= "HistoryOption"
        )
        st.session_state.Selected_History_Id =History_id_only(title_map=st.session_state.Title_maps,selected_title=st.session_state.HistoryOption)
        st.session_state.history_docs =history_query(st.session_state.Selected_History_Id)
        


                

    with AI_Note:
        try:
            st.session_state.AInote = st.session_state.history_docs[0][0]
            st.session_state.Question_with_context = st.session_state.history_docs[2][0]
        except:
            st.session_state.AInote = ["# Nothing yet"]

        for noted in st.session_state.AInote:  # Ai Note is a list
            st.markdown(noted)

    with Practice_test:
        st.session_state.chapter_count = "2"
        try:
            st.session_state.questions = st.session_state.history_docs[1][0]
        except:
            st.session_state.questions = ["# Nothing yet"]
        for question in st.session_state.questions:
            st.code(f" [SECTION] {st.session_state.questions.index(question) + 1}")
            st.markdown(question)

    st.session_state.user_inquiry = st.chat_input("Paste the test questions here to receive concise answers from my notes.")

    with Botly_replies:
        try:
            display_previous_chats(str(st.session_state.Selected_History_Id))
        except:
            pass
        
        if st.session_state.user_inquiry:
            success = user(st.session_state.user_inquiry)
            if success:
                bot_response(st.session_state.user_inquiry,st.session_state.Selected_History_Id)




































if st.session_state.user_info != False:
    auth_state = True
    pk_status = True   # check_if_pk_exists(PK=st.session_state.user_info["sub"],YourTableName="Users",yourPrimaryKeyColumn="UserID")

    if pk_status == True: # after first time logging in
        
        profile_completeness= True  # fk_status_profile_completeness(st.session_state.user_info['sub'])
        if profile_completeness ==True:
            main_ui()
            

                    
                    
    

                    
                    


   























if st.session_state.user_info == False:
    auth_state = False


        


