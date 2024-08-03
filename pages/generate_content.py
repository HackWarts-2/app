import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st

st.set_page_config(page_title="Generate Content", page_icon=":bulb:")

st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column-reverse;
        height: 60vh;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }
    .chat-input-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: fixed;
        bottom: 10px;
        width: 90%;
        background-color: #ffffff;
    }
    .chat-input {
        width: 100%;
        padding: 10px;
        margin-right: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .send-button {
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        background: linear-gradient(45deg, #ff6a00, #ee0979, #bd10e0);
        color: white;
        cursor: pointer;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #ff6a00, #ee0979, #bd10e0);
        border-radius: 10px;
    }
    .chat-container::-webkit-scrollbar {
        width: 10px;
    }
    .message-human {
        background-color: #F7F7F7;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: #8A3AB9; /* Instagram purple */
    }
    .message-ai {
        background-color: #E1306C; /* Instagram pink */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: white;
    }
    .stButton>button {
        background-color: #E1306C; /* Instagram pink */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stTextInput>div>div>input {
        border: 1px solid #E1306C; /* Instagram pink */
        background-color: #F7F7F7;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
      .navbar {
        background-color: #ff5733;
        padding: 1rem;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stTitle, .stHeader, .stSubheader {
        color: #405DE6; /* Instagram blue */
    }
    .stMarkdown {
        color: #E4405F; /* Instagram red */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="navbar">Cure Your Content Drought</div>', unsafe_allow_html=True)
st.header("Out of post ideas? We've got you covered with endless inspiration!🪄🪄")

memory = ConversationBufferMemory()

# Initialize session state variable for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
else:
    for message in st.session_state.chat_history:
        memory.save_context({'input': message['human']}, {'output': message['AI']})

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=['history', 'input'],
    template='''
You are an Instagram content creation expert. You give descriptive ideas to create interesting and engaging reels to increase engagement on Instagram account. 
Give reel ideas according to the description of the account which is ''' + st.session_state.query + '''. Give entire process and detailed description of what is to be done in the reel, including location where it is to be shot.
If any city or country is mentioned, add some cultural stuff in the reel ideas as well. Do not suggest to put popular hashtags, music.
Do not greet the user. Do not say Thank you. Give a list of reel ideas.Each idea should be on separate line. Do not show your enthusiasm.
Conversation history:
'{history}'
Human: '{input}'
AI:
    '''
)

ai71_api_key = os.getenv('AI71_TOKEN')
AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = ai71_api_key

llm = ChatOpenAI(
    model="tiiuae/falcon-180B-chat",
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
    streaming=True,
    temperature=0.7,
)

# Create the conversation chain
conversation_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=True)

# Function to process user input and generate response
def generate_response(user_input):
    response = conversation_chain({'input': user_input, 'history': st.session_state.chat_history})
    message = {'human': user_input, 'AI': response['text']}
    st.session_state.chat_history.append(message)

# Chat input and send button
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Enter your message here", key="user_input", placeholder="Type your message...")
    submit_button = st.form_submit_button(label="➤")
    
    if submit_button and user_input:
        generate_response(user_input)

# Display the conversation with emojis
with st.container():
    chat_container = st.container()
    with chat_container:
        for message in reversed(st.session_state.chat_history):
            st.markdown(f"<div class='message-human'>👤 : {message['human']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='message-ai'>🤖 : {message['AI']}</div>", unsafe_allow_html=True)
