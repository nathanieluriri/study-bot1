import streamlit as st
import time
from pathlib import Path
from langchain_community.chat_models import ChatOpenAI
from extraction import extract_text_from,Get_chunks
from variables import Get_questions,Get_Notes
#from dotenv import load_dotenv
#load_dotenv()

llm = ChatOpenAI(temperature=1,model="gpt-3.5-turbo-1106")



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


if not st.session_state.user_info == False:
    auth_state = True
    pk_status = True   # check_if_pk_exists(PK=st.session_state.user_info["sub"],YourTableName="Users",yourPrimaryKeyColumn="UserID")

    if pk_status == True: # after first time logging in
        
        profile_completeness= True  # fk_status_profile_completeness(st.session_state.user_info['sub'])
        if profile_completeness ==True:
            with st.sidebar:
                st.success(f" Welcome Back {st.session_state.user_info['given_name']}")
                
                if st.button("[TO Start a new session] ",type='primary'):
                    st.markdown("[Click me ](http://localhost:8501/)")

            Upload_PDFS, AI_Note, Practice_test = st.tabs(["Upload PDF's","AI Personalized Note","Practice Test"])


            with Upload_PDFS: # Upload documents tab
                with st.container(border=True):
                    st.session_state.note['content'] = st.file_uploader("Upload PDF's",type=["Pdf","Pptx","docx"],help="Upload PDFs or slide or word document to generate a personalized note",disabled=st.session_state.disabled)
                    if st.session_state.note['content'] != None:
                        st.warning("""
                                IF YOU CLICK CREATE MY NOTE YOU
                                 WILL HAVE TO START A NEW 
                                 SESSION TO CREATE ANOTHER NOTE!""",icon="⚠️")
                        if st.button("Create my note"):
                            st.session_state.note['status'] = 'In Progress'
                            st.session_state.disabled  = True
                            st.session_state.text_content = extract_text_from(st.session_state.note['content'])
                            
                            if st.session_state.text_content != None:
                                st.session_state.note['status'] = 'In Progress'
                                st.session_state.chunks = Get_chunks(st.session_state.text_content)
                                st.session_state.questions,st.session_state.Question_with_context =Get_questions(st.session_state.chunks)
                                
                                    
                       
                        
                        
                    
                        
            with AI_Note:
                if st.session_state.note['status']!= 'ready': # incase note isn't ready it should display something

                    if st.session_state.note['status'] == 'In Progress':
                         
                         st.info(f"CURRENT STATE : {st.session_state.note['status']}",icon="🔥")
                         st.session_state.AInote,st.session_state.note['status'] = Get_Notes(st.session_state.chunks)
                         st.write(f" Your Note Is {st.session_state.note['status']} Click the Button below to view it")
                         st.button("click me ! ")
                            
                    elif st.session_state.note['status'] != 'In Progress':
                        st.error(f"CURRENT STATE : {st.session_state.note['status']}",icon="🚨")

                elif st.session_state.note['status'] == 'ready':
                    st.success(f" {st.session_state.note['status']}",icon="🎁")
                    for noted in st.session_state.AInote:
                        st.markdown(noted)

            with Practice_test:
                st.session_state.chapter_count = "2"
                with st.container(border=True):
                    st.markdown("##### ~Greetings, everyone!~ Greetings Gabriel `How` are `you` `doing`? `Are` `you` `ready` `for` `the` `test`? `If` `you` `can` `confidently` `answer` `all` `the` `questions`, know that `you` `are` `prepared` `for` `anything`. Best of luck! ")

                if st.session_state.questions:
                    
                    for question in st.session_state.questions:
                        # st.session_state.chapter_count=+1
                        st.code(f" [SECTION] {st.session_state.questions.index(question)+1}")
                        st.markdown(question)
                        
                        


                
                










        else: # Complete profile 
            st.info("You can only submit values once")
            with st.container(border=True):
                
                st.subheader("Please complete your profile")
                tab1, tab2, tab3 = st.tabs(["Step 1", "Step 2", "Step 3"])
                with tab1:
                    st.code("text_for_tab_1")
                    st.slider(" ",1,5,key="reading_speed_slider",disabled=st.session_state.t1)
                    if st.button("Submit Reading Speed"):
                        st.session_state.t1 = True
                        st.write(st.session_state.reading_speed_slider)
                        
                    
                

                with tab2:
                    st.code("text_for_tab_2")
                    st.slider(" ",1,5,key="level_of_understanding_slider",disabled=st.session_state.t2)
                    if st.button("Submit Level Of Understanding"):
                        st.session_state.t2 = True
                        st.write(st.session_state.level_of_understanding_slider)

                with tab3:

                    st.code("text_for_tab_3" )
                    st.slider(" ",1,5,key="diction_slider",disabled=st.session_state.t3)
                    if st.button("Finish Profile"):
                        st.session_state.t3 = True
                        with st.spinner("Inserting Data into database..."):
                            # insert_into_ai_personalized_guide_for_users(st.session_state.user_info["sub"],st.session_state.reading_speed_slider,st.session_state.level_of_understanding_slider,st.session_state.diction_slider)
                            st.success("Succesfully Completed Profile weldone")

                        

                

    else: # First time logining in
        st.write(f"# Nice to meet you {st.session_state.user_info['name']}")
        # insert_into_user_reg(UserID=st.session_state.user_info["sub"],name=st.session_state.user_info["given_name"],email=st.session_state.user_info["email"] )
        st.success("You have Successfully logged in Please refresh and log in again")



if st.session_state.user_info == False:
    auth_state = False


        
if not st.session_state.user_info: # if user info is not true it would lead you to login
    st.write("# Please login to continue")



if auth_state == True: #debugging 
    pass
