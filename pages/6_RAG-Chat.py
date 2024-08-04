import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import openai
import streamlit as st
from utils import vector_search

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
st.header("Out of post ideas? We've got you covered with endless inspiration!✨💫")

# Define the categories
categories = [
    "Beauty & Skincare", "Fashion", "Food & Drink", "Health & Fitness", "Travel",
    "Lifestyle", "Photography", "Art", "Technology & Gadgets", "Business & Finance",
    "Entertainment", "Education & Learning", "Automotive", "Pets & Animals",
    "Home", "Garden", "Environmental & Social Issues", "Gaming", 
    "Events & Parties", "Books & Literature", "Miscellaneous"
]

# Form to select category and optionally input username
if 'category' not in st.session_state:
    with st.form(key='user_input_form'):
        selected_category = st.selectbox("Select a Category", options=categories)
        username = st.text_input("Instagram Username (Optional)")
        form_submit = st.form_submit_button(label="Submit")

        if form_submit:
            st.session_state['category'] = selected_category  # Save category to session state
            st.session_state['username'] = username  # Optionally save username to session state

# Only load chat functionality if the category is set
if 'category' in st.session_state:
    collection_name = {
        "Beauty & Skincare": "Beauty",
        "Food & Drink": "Food",
        "Health & Fitness": "Fitness",
        "Technology & Gadgets": "Tech",
        "Business & Finance": "Business_Finance",
        "Education & Learning": "Education",
        "Pets & Animals": "Pets",
        "Environmental & Social Issues": "Environmental",
        "Events & Parties": "Events",
        "Books & Literature": "Books",
        "Miscellaneous": "Misc",
        "Fashion": "Fashion",
        "Travel": "Travel",
        "Lifestyle": "Lifestyle",
        "Photography": "Photography",
        "Art": "Art",
        "Automotive": "Automotive",
        "Home": "Home",
        "Garden": "Garden",
        "Gaming": "Gaming",
        "Entertainment": "Entertainment"
    }.get(st.session_state['category'], None)

    if collection_name:
        st.write(f"Using collection: {collection_name}")
    else:
        st.error("Selected category does not have a corresponding collection in the database.")

    chat_memory = ConversationBufferMemory()

    # Initialize session state variable for chat history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    else:
        for message in st.session_state.conversation_history:
            chat_memory.save_context({'input': message['human']}, {'output': message['AI']})

    # Define the prompt template
    prompt_template_rag = PromptTemplate(
        input_variables=['history', 'input'],
        template='''
    You are an Instagram content creation expert. You have access to a vast amount of data about instagram profiles, posts and trends related to ''' + st.session_state['category'] + ''' category.
    Based on the user query, you will also be provided with relevant data from instagram profiles for the aforementioned category from the vector database.
    Answer using that information as well as your own expertise to give grounded responses.
    Do not greet the user. Do not say Thank you. Do not show your enthusiasm.
    Conversation history:
    '{history}'
    Human: '{input}'
    AI:
        '''
    )

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

    # Create the conversation chain
    conversation_chain_rag = LLMChain(llm=llm, prompt=prompt_template_rag, memory=chat_memory, verbose=True)

    # Function to process user input and generate response
    def generate_response(user_input):

        def combine_search_results(search_results):
            combined_content = ""
            for result in search_results:
                content = result.get('content', '')
                combined_content += content + "\n\n"  # Add extra spacing between contents
            return combined_content.strip()

        def extract_references(search_results):
            references = []
            for i, result in enumerate(search_results):
                post_url = result.get('postURL', '')
                profile_url = result.get('profileURL', '')
                reference = f"Reference {i+1}:"
                if post_url:
                    reference += f"\n- Post URL: [{post_url}]({post_url})"
                if profile_url:
                    reference += f"\n- Profile URL: [{profile_url}]({profile_url})"
                if reference != f"Reference {i+1}:":  # Ensure there is content to show
                    references.append(reference)
            return "\n\n".join(references)

        # Perform vector search based on user input and collection name
        search_results = vector_search(user_input, collection_name)
        print(search_results)
        
        # Combine the content of all search results
        combined_content = combine_search_results(search_results)
        
        # Extract references from search results
        references = extract_references(search_results)
        print(references)

        # Prepare input for the model
        augmented_input = f"User: {user_input}. Retrieved context: {combined_content}"
        
        response = conversation_chain_rag({'input': augmented_input, 'history': st.session_state.conversation_history})
        
        # Append references to the response text
        final_response = response['text']
        if references:
            final_response += "\n\n**REFERENCES**:\n" + references

        message = {'human': user_input, 'AI': final_response}
        st.session_state.conversation_history.append(message)

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
            for message in (st.session_state.conversation_history):
                if 'human' in message:                           
                    st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='message-human'>👤<br> {message['human']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='message-ai'>🤖<br> {message['AI']}</div>", unsafe_allow_html=True)