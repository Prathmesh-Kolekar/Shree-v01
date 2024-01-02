import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

# Load environment variables from .env
load_dotenv()

# Set the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', default="your_default_api_key")
genai.configure(api_key=GOOGLE_API_KEY)

model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)

template = """The following is a friendly conversation between a human and an AI. The AI named Shree is talkative and provides lots of specific details from its context which can also serve as conversation history to remember previous responses and dont generate anything else if you dont know say so.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

st.title("Shree-v01")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Greetings , How may I help you"
        }
    ]

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationBufferWindowMemory(k=3, ai_prefix="AI Assistant")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a conversation chain with the specified conversation memory
conversation = ConversationChain(
    prompt=PROMPT,
    llm=model,
    memory=st.session_state.conversation_memory,
)

# Process and store Query and Response
def llm_function(query):
    ans = conversation.predict(input=query)

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(ans)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ans
        }
    )

# Accept user input
query = st.chat_input("Enter Your Message")

# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)
