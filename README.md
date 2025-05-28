# 🤖 AI Powered Virtual Assistant

An intelligent voice assistant powered by Open Source LLaMA 3.1, integrated with speech recognition and text-to-speech features. This virtual assistant can listen to your voice, respond with AI-generated answers, and speak the response aloud.

---

## 🚀 Features

- 🎤 **Speech-to-Speech Mode**  
  Speak your query, and the assistant will listen, process using LLaMA 3.1, and speak the answer.  
  ⚠️ **Note:** *Speech-to-Speech mode has not been fully tested yet. Further testing is needed for robustness and real-time interaction reliability.*

- 💬 **Text-to-Speech Mode**  
  Type your query, and get a spoken response.

- 🧠 **LLaMA 3.1 Integration**  
  Utilizes a local LLaMA 3.1 model to generate intelligent responses.

- 🔊 **Text-to-Speech Engine**  
  Reads out the assistant’s response using `pyttsx3`.

- 🛑 **Stop Button (Optional)**  
  Gracefully halts speaking mid-response (code available but currently commented out).

---

## 🛠️ Tech Stack

| Component         | Technology            |
|------------------|------------------------|
| Frontend UI      | Streamlit              |
| Speech-to-Text   | SpeechRecognition (Google API) |
| Text-to-Speech   | pyttsx3                |
| AI Backend       | Local LLaMA 3.1 via `ollama` |
| HTTP Requests    | Requests Library       |
| Multithreading   | Python `threading`     |

---
