import streamlit as st
import uuid
import time
from langchain_community.chat_message_histories import SQLChatMessageHistory
from bot_logic import load_vector_store, create_conversational_rag_chain

st.set_page_config(page_title="Case Interview/Guesstimates Simulator", layout="centered")
st.title(" Case Interview/Guesstimates Simulator 🧠")
st.sidebar.title("Options")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

chat_history = SQLChatMessageHistory(
    session_id=st.session_state.session_id, 
    connection="sqlite:///chat_history.db"
)


@st.cache_resource
def get_rag_chain():
    vector_store = load_vector_store()
    return create_conversational_rag_chain(vector_store)

rag_chain = get_rag_chain()

for msg in chat_history.messages:
    st.chat_message(msg.type).write(msg.content)

def fake_stream(text, delay=0.02):
    for word in text.split():
        yield word + " "
        time.sleep(delay)

if st.sidebar.button("Generate Case"):
    with st.spinner("Generating case..."):
        case_interviewer_prompt = """
You are a senior consultant at a top-tier consulting firm. Your task is to generate realistic opening statements for business case interviews, just like an actual interviewer would begin a case.

Use the knowledge and context of real consulting cases to craft diverse case openings. Each case should fall into one of the following categories:
- Profitability (e.g., declining revenues, increasing costs, etc.)
- Market Entry (e.g., new product, new geography, new service)
- Mergers & Acquisitions (e.g., target identification, synergy analysis, due diligence)
- Growth Strategy (e.g., market share increase, new product line, expansion)
- Pricing (e.g., new product pricing, existing product repricing)

Each opening should:
- Briefly introduce a real-world-style client (industry, geography, size, etc.)
- Clearly present a core business challenge, often with a key metric or data point.
- End with a professional prompt like “How would you approach this?” or “What would you like to know first?”

The tone should be professional, neutral, and similar to that of an MBB interviewer.

Example:
"Your client is a European ride-sharing company that has seen a 25% drop in customer retention over the past year. They want to understand the root cause and fix it. What would you like to know first?"

Only generate one new case opening at a time. """
        
        try:
            user_prompt = "Generate a new case for me"
            st.chat_message("user").write(user_prompt)
            chat_history.add_user_message(user_prompt)

            response = rag_chain.invoke({
                "chat_history": chat_history.messages,
                "input": user_prompt,
                "system_prompt": case_interviewer_prompt
            })
            ai_response = response["answer"]

            st.chat_message("assistant").write_stream(fake_stream(ai_response))
            chat_history.add_ai_message(ai_response)
        except Exception as e:
            st.error(f"Error: {e}")

if st.sidebar.button("Generate Guesstimate"):
    with st.spinner("Generating guesstimate..."):
        interviewer_prompt = """
You are a sharp, no-nonsense consulting case interviewer for a top-tier firm like McKinsey, Bain, or BCG.

Your task is to simulate a real interview, using the given context as your knowledge base. The context will include one or more guesstimate or business case questions. Here’s how to behave:

Instructions:
- Act as the human interviewer, not a bot or tutor.
- Pick one question from the context and present it as a real-time prompt to the candidate.
- Allow the candidate to ask clarifying questions or begin reasoning.
- Ask probing questions, challenge flawed assumptions, and steer them without giving away answers.
- Keep the tone professional but slightly tough — like a real interviewer.
- If the candidate gets stuck, nudge them forward subtly.
- At the end of the question, give a quick but useful feedback summary on:
  - Structure
  - Clarity of assumptions
  - Approximations and sanity of logic

You are not allowed to invent new questions unless the context does not provide any. Stay grounded in the context.

Start by saying: 
“Alright, let’s begin with a guesstimate.”
"""
        
        try:
            user_prompt = "Generate a new guesstimate for me"
            st.chat_message("user").write(user_prompt)
            chat_history.add_user_message(user_prompt)

            response = rag_chain.invoke({
                "chat_history": chat_history.messages,
                "input": user_prompt,
                "system_prompt": interviewer_prompt
            })
            ai_response = response["answer"]
            
            st.chat_message("assistant").write_stream(fake_stream(ai_response))
            chat_history.add_ai_message(ai_response)
        except Exception as e:
            st.error(f"Error: {e}")

if st.sidebar.button("Explain A Topic"):
    with st.spinner("Explaining topic..."):
        case_concept_explainer_prompt = """
You are a top consulting coach and expert in case interview prep. Your role is to clearly explain key consulting concepts, frameworks, and business fundamentals using the context retrieved from the RAG vector database.

Your response should:
- Be structured and easy to understand
- Use examples when helpful
- Avoid unnecessary jargon
- Be precise, as if explaining to someone preparing for McKinsey, BCG, or Bain interviews

Stick only to the information provided by the RAG context — do not hallucinate.

If the concept has multiple variations or frameworks (e.g., profitability trees, growth levers), break them down logically.

At the end, ask: “Would you like an example case where this applies?”

Respond as a friendly and knowledgeable mentor.
"""
        
        try:
            user_prompt = "Explain a topic for me"
            st.chat_message("user").write(user_prompt)
            chat_history.add_user_message(user_prompt)

            response = rag_chain.invoke({
                "chat_history": chat_history.messages,
                "input": user_prompt,
                "system_prompt": case_concept_explainer_prompt
            })
            ai_response = response["answer"]
            
            st.chat_message("assistant").write_stream(fake_stream(ai_response))
            chat_history.add_ai_message(ai_response)
        except Exception as e:
            st.error(f"Error: {e}")

if st.sidebar.button("Reset Chat", type="primary"):
    chat_history.clear()
    st.rerun()

    
if user_input := st.chat_input("Enter your response here..."):
    st.chat_message("user").write(user_input)
    chat_history.add_user_message(user_input)
    
    with st.spinner("Thinking..."):
        try:
            response = rag_chain.invoke({
                "chat_history": chat_history.messages,
                "input": user_input
            })
            ai_response = response["answer"]
        except Exception as e:
            ai_response = "Oops! Something went wrong. Please try again."
            st.error(f"Error: {e}")
    
    st.chat_message("assistant").write_stream(fake_stream(ai_response))
    chat_history.add_ai_message(ai_response)