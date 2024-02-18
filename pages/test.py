import time
import streamlit as st
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx

def function1():
    for i in range(5):
        time.sleep(1)
        print(f"function 1 {i}")

def function2():
    for i in range(5):
        time.sleep(0.5)
        print(f"Function 2: {i}")

def run_thread(target_function):
    t = Thread(target=target_function)
    add_script_run_ctx(t)
    t.start()

if __name__ == "__main__":
    st.title("Streamlit Multi-threading Example")

    # Run function1 in a thread
    run_thread(function1)

    # Run function2 in a thread
    run_thread(function2)
