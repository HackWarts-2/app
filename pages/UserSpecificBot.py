import streamlit as st

def main():
    st.set_page_config(page_title="INSTArget", page_icon=":rocket:")

    # Sidebar styling
    sidebar_style = """
    <style>
    .sidebar .sidebar-content {
        font-family: 'Arial', sans-serif;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
    }
    .sidebar .sidebar-content h2 {
        color: #ff6b6b;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content p {
        color: #4b4b4b;
        font-size: 16px;
    }
    .navbar {
        background-color: #e56969;
        padding: 1rem;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #e56969;
    .stButton>button {
        background-color: #e56969;  
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .bold {
        font-weight: bold;
    }
    </style>
    """
    
    st.markdown(sidebar_style, unsafe_allow_html=True)
    st.markdown('<div class="navbar">"INSTArget🎯"</div>', unsafe_allow_html=True)
    
    
    st.write("**Targeted Insights and Tailored Support for Your Instagram Journey: Discover, Analyze, and Create with Precision!**")

    st.subheader("Your Navigation to the Best Insta Profile:")

   
    with st.sidebar:
        st.markdown("<div class='sidebar-content'><h2>INSTArget🎯</h2>", unsafe_allow_html=True)
        st.markdown("<p>Boost your Instagram game with tailored, fun analysis and insights.</p></div>", unsafe_allow_html=True)
    st.sidebar.page_link('pages/1_details.py', label='Details')
    st.sidebar.page_link('pages/2_similar_profiles.py', label='Similar Profiles')
    st.sidebar.page_link('pages/4_generate_content.py', label='Create Content')
    st.sidebar.page_link('pages/6_RAG-Chat.py', label='Ask Me')

   
    if st.button("Get Started"):
        st.switch_page("pages/1_details.py")
if __name__ == "__main__":
    main()
