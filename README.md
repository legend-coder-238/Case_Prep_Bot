# 🧠 Case Prep Bot – Your AI-Powered Case Interview & Guesstimate Simulator

> An advanced, interactive, and RAG-powered chatbot that helps you master consulting case interviews, guesstimates, and business frameworks using real casebooks and AI.

---

## 🎯 Vision

- Empower students and consulting aspirants with **realistic case simulations**
- Use **context-aware GenAI** + **vector databases** for precision
- Mimic the **MBB-style interview** experience
- Make case prep less boring and more effective

---

## 🚀 Core Features

### 🧑‍💼 Case Interview Simulator
- Generates **structured case prompts** (Profitability, Market Entry, M&A, etc.)
- Simulates real interviewer follow-ups
- Built using **LangChain**, **Gemini API**, and **Qdrant**

---

### 📊 Guesstimate Generator
- Pulls actual guesstimates from casebooks using **RAG**
- Challenges the user with **step-by-step probing**
- Provides feedback on **structure, assumptions & logic**

---

### 📚 Concept Explainer
- Explains consulting frameworks & business concepts
- Only uses **verified context from uploaded casebooks**
- Optionally suggests example cases for practice

---

## ⚙️ How It Works

- **Data Source**: Casebooks are parsed & chunked using `unstructured`
- **Vector Store**: Embeddings stored in **Qdrant Cloud**
- **LLM**: Gemini 2.0 Flash via `langchain-google-genai`
- **Frontend**: Streamlit app with chat interface + sidebar controls
- **Memory**: Conversation history stored in **SQLite**

---

## 📦 Tech Stack

**Frontend**: Streamlit  
**Backend**: Python, LangChain, Gemini API  
**Embedding Model**: `BAAI/bge-large-en`  
**Vector DB**: Qdrant  
**PDF Parsing**: `unstructured`, `rembg`  
**Storage**: SQLite for chat history  
**Deployment-ready**: Can be containerized & hosted via Streamlit Cloud, Railway, or any VM

---

## 🧪 Sample Prompts

> **Case Prompt**: "Your client is a food delivery startup in Southeast Asia. Revenues are flatlining. What would you like to know first?"

> **Guesstimate Prompt**: "Estimate the number of umbrellas sold annually in Mumbai."

> **Concept Prompt**: "Explain the profitability framework and when to apply it."

---

## 🧙 Team Member

- **Ankur** – IIT Delhi | GenAI + Strategy Enthusiast

---

## 🚧 Roadmap

- [x] Case/Guesstimate/Topic modules  
- [x] Chat memory persistence  
- [ ] Light/Dark mode toggle  
- [ ] Responsive design polish  
- [ ] Add custom case upload option  
- [ ] Deployment on HuggingFace / Streamlit Cloud

---

## ⚡ Getting Started

```bash
git clone https://github.com/legend-coder-238/Case_Prep_Bot.git
cd Case_Prep_Bot
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
