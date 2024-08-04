import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

import os
st.set_page_config(page_title="Generate Content", page_icon=":bulb:")
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 60vh;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 10px;
        background-color: #f9f9f9;
        margin-bottom: 70px; /* Add margin to make space for the fixed input */
    }
    .chat-input-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: fixed;
        bottom: 10px;
        width: 90%;
        background-color: #ffffff;
        padding: 10px;
        border-top: 1px solid #ccc; /* Add a top border for better visibility */
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
        color: ##e56969;
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
        color: #8a49a1; /* Instagram purple */
        color: #8a49a1; /* Instagram purple */
    }
    .message-ai {
        background-color: #c1888b;  
        background-color: #8a49a1;  
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: white;
    }
    .stButton>button {
        background-color: ##e56969;
     .stButton>button {
        background-color: #e56969;  
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stTextInput>div>div>input {
        border: 1px solid #c1888b;
        border: 1px solid #c1888b;
        background-color: #F7F7F7;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .navbar {
        background-color: #8a49a1;
        background-color: #8a49a1;
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
def main():
    st.markdown('<div class="navbar">Cure Your Content Drought</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Reels", "Posts", "Stories"])
    ai71_api_key = st.secrets['AI71_TOKEN']
    #ai71_api_key = os.getenv('AI71_TOKEN')
    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = ai71_api_key

    llm = ChatOpenAI(
                model="tiiuae/falcon-180B-chat",
                api_key=AI71_API_KEY,
                base_url=AI71_BASE_URL,
                streaming=True,
                temperature=0.7,
            )
    with tabs[0]:
        if 'query' in st.session_state:
            st.header("Out of post ideas? We've got you covered with endless inspiration!✨💫")
            
            
            memory = ConversationBufferMemory()

            # Initialize session state variable for chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            for message in st.session_state.chat_history:
                if 'human' in message:
                    memory.save_context({'input': message['human']}, {'output': message['AI']})
                else:
                    memory.save_context({'input': "give reel ideas!"}, {'output': message['AI']})

            # Define the prompt template
            prompt_template = PromptTemplate(
                input_variables=['history', 'input'],
                template='''
You are an Instagram content creation expert. You give descriptive ideas to create interesting and engaging reels to increase engagement on Instagram account. 
Give reel ideas according to the description of the account which is ''' + st.session_state.query + '''.For each idea,give entire process and detailed description of what is to be done in the reel,and include a setup details where the reel should be shot. Suggest different setups for every idea.Do not suggest one setup more than twice.
If any city or country name is mentioned, add some cultural stuff in the reel ideas as well. Do not suggest to put popular hashtags, music.
Do not greet the user. Do not say Thank you.Do not mention the statement "''' + st.session_state.query + '''".Do not mention the work "City".
Do not mention the word "Country". Do not show your enthusiasm.Return a list of bulleted ideas of reels.Each idea should begin from a separate line.Do not mention the word "Idea".
Conversation history:
'{history}'
Human: '{input}'
AI:
                '''
            )

            

            # Create the conversation chain
            conversation_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=True)

            # Function to process user input and generate response
            def generate_response(user_input):
                with st.spinner('Fetching some cool reel ideas...'):
                    response = conversation_chain({'input': user_input, 'history': st.session_state.chat_history})
                    if st.session_state.chat_history == []:
                        message = {'AI': response['text']}
                    else:
                        message = {'human': user_input, 'AI': response['text']}
                    st.session_state.chat_history.append(message)

            # Chat input and send button
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input("Enter your message here", key="user_input", placeholder=" Ask Anything.......")
                submit_button = st.form_submit_button(label="➤")
                if st.session_state.chat_history == []:
                    generate_response("give reel ideas!")
                else:
                    if submit_button and user_input:
                        generate_response(user_input)

            # Display the conversation with emojis
            with st.container():
                chat_container = st.container()
                with chat_container:
                    for message in (st.session_state.chat_history):
                        if 'human' in message:
                            st.markdown(f"<div class='message-human'>👤<br>  {message['human']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)    

        else:
            st.write("Fill the details form first.")
    
    with tabs[1]:
        if 'query' in st.session_state:
            st.header("Out of post ideas? We've got you covered with endless inspiration!✨💫")
            
            
            memory = ConversationBufferMemory()

            # Initialize session state variable for chat history
            if 'posts_chat_history' not in st.session_state:
                st.session_state.posts_chat_history = []
            
            for message in st.session_state.posts_chat_history:
                if 'human' in message:
                    memory.save_context({'input': message['human']}, {'output': message['AI']})
                else:
                    memory.save_context({'input': "give posts ideas!"}, {'output': message['AI']})

            # Define the prompt template
            prompt_template = PromptTemplate(
                input_variables=['history', 'input'],
                template='''
You are an Instagram content creation expert. You give descriptive ideas to create interesting and engaging posts to increase engagement on Instagram account. 
Give post ideas according to the description of the account.Description of the account is:''' + st.session_state.query + '''. Give entire detailed process and detailed description of what is to be shown in the post.
For each post idea,  show how the picture is to be taken, and include potential setups or location spots. Donot suggest one location spot more than twice.
If any city or country is mentioned, add some cultural stuff in the post ideas as well.Do not add the words "Cultural Stuff". Also give captions to put under the posts.Do not suggest to put popular hashtags, music.Do not give hashtags.
Do not greet the user. Do not say Thank you.Do not mention the statement "''' + st.session_state.query + '''".Do not mention the word "City".Do not mention the word "Country".
 Do not show your enthusiasm.
 Return a list of bulleted ideas of posts. Each idea should begin on a separate line.
 Do not show your enthusiasm.
 Return a list of bulleted ideas of posts. Each idea should begin on a separate line.Do not mention the word "Idea".
Conversation history:
'{history}'
Human: '{input}'
AI:
                '''
            )
            # Create the conversation chain
            conversation_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=True)

            # Function to process user input and generate response
            def generate_response(user_input):
                with st.spinner('Post inspo incoming...'):
                    response = conversation_chain({'input': user_input, 'history': st.session_state.posts_chat_history})
                    if st.session_state.posts_chat_history == []:
                        message = {'AI': response['text']}
                    else:
                        message = {'human': user_input, 'AI': response['text']}
                    st.session_state.posts_chat_history.append(message)

            # Chat input and send button
            with st.form(key='post_chat_form', clear_on_submit=True):
                user_input = st.text_input("Enter your message here", key="posts_user_input", placeholder=" Ask Anything.......")
                submit_button = st.form_submit_button(label="➤")
                if st.session_state.posts_chat_history == []:
                    generate_response("give post ideas!")
                else:
                    if submit_button and user_input:
                        generate_response(user_input)

            # Display the conversation with emojis
            with st.container():
                chat_container = st.container()
                with chat_container:
                    for message in (st.session_state.posts_chat_history):
                        if 'human' in message:
                            st.markdown(f"<div class='message-human'>👤<br> {message['human']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)
                            
                        else:
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)  
    
    with tabs[2]:
        if 'query' in st.session_state:
            st.header("Out of post ideas? We've got you covered with endless inspiration!✨💫")
            
            
            memory = ConversationBufferMemory()

            # Initialize session state variable for chat history
            if 'stories_chat_history' not in st.session_state:
                st.session_state.stories_chat_history = []
            
            for message in st.session_state.stories_chat_history:
                if 'human' in message:
                    memory.save_context({'input': message['human']}, {'output': message['AI']})
                else:
                    memory.save_context({'input': "give instagram story ideas!"}, {'output': message['AI']})

            # Define the prompt template
            prompt_template = PromptTemplate(
                input_variables=['history', 'input'],
                template='''
You are an Instagram content creation expert. You give descriptive ideas to create interesting and engaging instagram stories. Donot mention the word "Posts".
Give story ideas according to the description of the account.Description of the account is: ''' + st.session_state.query + '''.
For each story idea, Give entire detailed process and detailed description of what is to be shown in the stories.
Return the results in a timeline based story posting suggestion. For each idea, show how the pictures in the stories are to be taken, 
and displayed and include any potential location spots or setups.
If any city or country is mentioned, add some cultural stuff in the story ideas as well. Suggest captions to put on the stories.
Do not suggest to put popular hashtags, music.Do not give hashtags.Do not mention the word "Story Idea".
Do not greet the user. Do not say Thank you.Do not mention the statement "''' + st.session_state.query + '''".Do not mention the word "City".Do not mention the word "Country". Do not show your enthusiasm.
Return a list of bulleted ideas of stories only. Each idea should begin on a separate line.
Do not suggest to put popular hashtags, music.Do not give hashtags.
Do not greet the user. Do not say Thank you.Do not mention the statement "''' + st.session_state.query + '''".Do not mention the word "City".Do not mention the word "Country". Do not show your enthusiasm.
Return a list of bulleted ideas of stories only. Each idea should begin on a separate line.Do not mention the word "Idea".
Conversation history:
'{history}'
Human: '{input}'
AI:
                '''
            )

            

            # Create the conversation chain
            conversation_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory, verbose=True)

            # Function to process user input and generate response
            def generate_response(user_input):
                with st.spinner('Spinning up aesthetic story ideas...'):
                    response = conversation_chain({'input': user_input, 'history': st.session_state.stories_chat_history})
                    if st.session_state.stories_chat_history == []:
                        message = {'AI': response['text']}
                    else:
                        message = {'human': user_input, 'AI': response['text']}
                    st.session_state.stories_chat_history.append(message)

            # Chat input and send button
            with st.form(key='story_chat_form', clear_on_submit=True):
                user_input = st.text_input("Enter your message here", key="story_user_input", placeholder=" Ask Anything.......")
                submit_button = st.form_submit_button(label="➤")
                if st.session_state.stories_chat_history == []:
                    generate_response("give post ideas!")
                else:
                    if submit_button and user_input:
                        generate_response(user_input)

            # Display the conversation with emojis
            with st.container():
                chat_container = st.container()
                with chat_container:
                    for message in (st.session_state.stories_chat_history):
                        if 'human' in message:
                            st.markdown(f"<div class='message-human'>👤<br> {message['human']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)
                            
                        else:
                            st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)   

if __name__ == "__main__":
    main()
