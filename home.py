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
    .bold {
        font-weight: bold;
    }
    </style>
    """
    
    st.markdown(sidebar_style, unsafe_allow_html=True)

    st.title("INSTArget🎯")
    
    st.write("**Targeted Insights and Tailored Support for Your Instagram Journey: Discover, Analyze, and Create with Precision!**")

    st.subheader("Your Navigation to the Best Insta Profile:")

    st.write('<span class="bold">🚀 Start Your Journey:</span> ', unsafe_allow_html=True)
    st.write(' Begin on the details page and hit \'Done\'✅ to discover profiles that align with your vibe. You\'ll be redirected to the \'Similar Profiles\' page.', unsafe_allow_html=True)
    st.write('<span class="bold">🔍 Explore Similar Profiles:</span>', unsafe_allow_html=True)
    st.write('Click "Get Insights"  of any profile to unlock their latest posts secrets.🕵', unsafe_allow_html=True)
    st.write(' Alternatively, Hit \'Ask Anything\' on a profile to chat with our bot about that specific Instagram account.', unsafe_allow_html=True)
    st.write('<span class="bold">🤖 Engage with Our Bot:</span>  ', unsafe_allow_html=True)
    st.write('Chat with our bot!Discover general trends, trendy deals, upcoming events, and more!📅', unsafe_allow_html=True)
    st.write("You can also pass in a username if you want to specifically ask about a profile to see what they're up to.📝", unsafe_allow_html=True)
    st.write('<span class="bold">💡 Generate Content Ideas:</span> ', unsafe_allow_html=True)
    st.write('Get a list of content ideas for your next posts,reels and even stories!🤌', unsafe_allow_html=True)
    st.write('Use our content specialist chatbot to get fresh inspiration.💭 Ask about trending topics for reels, posts, and stories, and keep the conversation flowing for endless content tips!', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("<div class='sidebar-content'><h2>INSTArget🎯</h2>", unsafe_allow_html=True)
        st.markdown("<p>Boost your Instagram game with tailored, fun analysis and insights.</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
