def main( user_info, disabled,   Question_with_context, questions, AInote):
    with st.sidebar:
        run_once()
        
        
        st.session_state.user_info = user_info

            if user_info:
                st.session_state.signed_in = True
                
            else:
                st.session_state.signed_in = False

    if st.session_state.signed_in:
        st.info("Use the test questions generated for quick answers from Botly. Check notes if needed. The function would be made available once the notes are generated", icon="✔")
        with st.sidebar:
            st.success(f" Welcome Back {user_info['given_name']}")
            if st.button("[TO Start a new session] ", type='primary'):
                st.markdown("[Click me ](/)")

        Upload_PDFS, AI_Note, Practice_test, Botly_replies = st.tabs(["Upload PDF's", "AI Personalized Note", "Practice Test", "Botly replies"])

        with Upload_PDFS:
            with st.container(border=True):
                note['content'] = st.file_uploader("Upload PDF's",
                                                   type=["Pdf", "Pptx", "docx"],
                                                   help="Upload PDFs or slides or word documents to generate a personalized note",
                                                   disabled=disabled)


        with AI_Note:
            st.success(f" {note['status']}", icon="🎁")
            for noted in AInote:
                st.markdown(noted)

        with Practice_test:
            with st.container(border=True):
                st.markdown(
                    "##### ~Greetings, everyone!~ Greetings Gabriel `How` are `you` `doing`? `Are` `you` `ready` `for` `the` `test`? `If` `you` `can` `confidently` `answer` `all` `the` `questions`, know that `you` `are` `prepared` `for` `anything`. Best of luck! ")

            if questions:
                for question in questions:
                    st.code(f" [SECTION] {questions.index(question) + 1}")
                    st.markdown(question)

            user_inquiry = st.chat_input(
                "Paste the test questions here to receive concise answers from my notes.")

            with Botly_replies:
                display_previous_chats()# should take previous messages as a parameter
                if user_inquiry:
                    success = user(user_inquiry)
                    if success:
                        bot_response(user_inquiry)

                else:
                    print(user_inquiry)




if __name__ == "__main__":
    main(
        
        user_info=st.session_state.user_info,
        disabled=True,
        Question_with_context=st.session_state.Question_with_context,
        questions=st.session_state.questions,
        AInote=st.session_state.AInote
    )
