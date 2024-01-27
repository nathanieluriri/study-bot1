

def main(signed_in, user_info, disabled, Prompt, messages, note, text_content, Question_with_context, questions, AInote):
    with st.sidebar:
        run_once()

        if not signed_in:
            user_info = {'given_name': 'Gabriel'}
            st.session_state.user_info = user_info

            if user_info:
                st.session_state.signed_in = True
            else:
                st.session_state.signed_in = False

    auth_state = None

    if st.session_state.signed_in:
        auth_state = True
        pk_status = True
        if pk_status:
            profile_completeness = True
            if profile_completeness:
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
                        if note['content'] is not None:
                            st.warning("""
                                    IF YOU CLICK CREATE MY NOTE YOU
                                     WILL HAVE TO START A NEW 
                                     SESSION TO CREATE ANOTHER NOTE!""", icon="⚠️")
                            if st.button("Create my note"):
                                note['status'] = 'In Progress'
                                disabled = True
                                text_content = extract_text_from(note['content'])

                                if text_content is not None:
                                    note['status'] = 'In Progress'
                                    chunks = Get_chunks(text_content)
                                    questions, Question_with_context = Get_questions(chunks)

                with AI_Note:
                    if note['status'] != 'ready':

                        if note['status'] == 'In Progress':
                            st.info(f"CURRENT STATE : {note['status']}", icon="🔥")
                            AInote, note['status'] = Get_Notes(chunks)
                            st.write(
                                f" Your Note Is {note['status']} Click the Button below to view it")
                            st.button("click me ! ")

                        elif note['status'] != 'In Progress':
                            st.error(f"CURRENT STATE : {note['status']}", icon="🚨")

                    elif note['status'] == 'ready':
                        st.success(f" {note['status']}", icon="🎁")
                        for noted in AInote:
                            st.markdown(noted)

                with Practice_test:

                    st.session_state.chapter_count = "2"
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
                    display_previous_chats()
                    if user_inquiry:
                        success = user(user_inquiry)
                        if success:
                            bot_response(user_inquiry)

                    else:
                        print(user_inquiry)

    else:
        st.write(f"# Nice to meet you {user_info['name']}")
        st.success("You have Successfully logged in Please refresh and log in again")

    check_user_info()

    if auth_state == True:
        pass


if __name__ == "__main__":
    main(
        signed_in=st.session_state.signed_in,
        user_info=st.session_state.user_info,
        disabled=st.session_state.disabled,
        Prompt=st.session_state.Prompt,
        messages=st.session_state.messages,
        note=st.session_state.note,
        text_content=st.session_state.text_content,
        Question_with_context=st.session_state.Question_with_context,
        questions=st.session_state.questions,
        AInote=st.session_state.AInote
    )
