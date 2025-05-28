import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import json
import threading

# Global control flag
stop_speaking_flag = False
speech_thread = None

def speak(text):
    global stop_speaking_flag, speech_thread

    # Define the speech function
    def run_speech():
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', 160)
        local_engine.say(text)

        try:
            local_engine.runAndWait()
        except RuntimeError:
            pass

    # Stop any previous speech
    stop_speaking()

    # Start new speech only if none is running
    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()

def stop_speaking():
    global stop_speaking_flag, speech_thread

    stop_speaking_flag = True
    if speech_thread and speech_thread.is_alive():
        # pyttsx3 does not support clean mid-speech stop, so we use a new engine next time
        try:
            pyttsx3.init().stop()  # Try to stop any running instance
        except Exception:
            pass
        speech_thread.join(timeout=1)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {query}")
        return query
    except sr.UnknownValueError:
        st.error("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        st.error("Speech service is down.")
        return ""

def generate_response(query):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.1",
        "prompt": f"Answer in 1–2 simple, clear sentences. Avoid jargon. Question: {query}",
        "stream": False
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(data))
        if res.status_code == 200:
            response_text = res.json().get("response", "Sorry, I couldn't find an answer.")
            return response_text.strip()
        else:
            return f"Error from LLaMA: {res.status_code}"
    except Exception as e:
        return f"Connection error: {e}"

# Streamlit UI
st.set_page_config(page_title="🎙️ AI Voice Assistant with Stop Button")
st.title("🧠 Your AI Voice Assistant ")
st.markdown("Use **speech or text**, and I’ll answer ")

mode = st.radio("Choose Mode:", ["Speech-to-Speech", "Text-to-Speech"])

if mode == "Speech-to-Speech":
    col1, col2 = st.columns(2)
    if col1.button("🎤 Speak Now"):
        query = listen()
        if query:
            response = generate_response(query)
            st.info(f"🤖 Assistant: {response}")
            speak(response)

    # if col2.button("🛑 Stop"):
    #     stop_speaking()
    #     st.warning("Speech stopped manually.")

elif mode == "Text-to-Speech":
    user_input = st.text_input("💬 Enter your query")
    col1, col2 = st.columns(2)
    if col1.button("🚀 Submit"):
        if user_input:
            response = generate_response(user_input)
            st.info(f"🤖 Assistant: {response}")
            speak(response)
    # if col2.button("🛑 Stop"):
    #     stop_speaking()
    #     st.warning("Speech stopped manually.")
# Ensure the speech thread is cleaned up on exit