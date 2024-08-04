import streamlit as st
import streamlit.components.v1 as components

# Define custom CSS for Instagram-like theme
custom_css = """
<style>
    body {
        background-color: #fafafa;
    }
    .stApp {
        background-color: #fafafa;
    }
    .navbar {
        background-color: #8a49a1;
        padding: 1rem;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .sidebar-font{
                color:black}
    .stMarkdown {
        color: #E4405F; /* Instagram red */
    }
    .post-insight {
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .post-url {
        color: #833AB4; /* Instagram gradient color */
        font-weight: bold;
    }
    .insight-text {
        color: #5851DB; /* Instagram gradient color */
        margin-bottom: 1rem;
    }
</style>
"""

def main():
    st.set_page_config(page_title="Profile Details", page_icon=":bust_in_silhouette:")
    with st.sidebar:
        st.markdown("<div class='sidebar-content'><h2>INSTArget🎯</h2>", unsafe_allow_html=True)
        st.markdown("<p class='sidebar-font'>Boost your Instagram game with tailored, fun analysis and insights.</p></div>", unsafe_allow_html=True)
    st.sidebar.page_link('pages/1_details.py', label='Details')
    st.sidebar.page_link('pages/2_similar_profiles.py', label='Similar Profiles')
    st.sidebar.page_link('pages/4_generate_content.py', label='Create Content')
    st.sidebar.page_link('pages/6_RAG-Chat.py', label='Ask Me')
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Navbar
    st.markdown('<div class="navbar">Profile Details</div>', unsafe_allow_html=True)

    # Access the selected profile insights and URL from session state
    if 'selected_profile_insights' in st.session_state and 'selected_profile_url' in st.session_state:
        insights = st.session_state['selected_profile_insights']
        profile_url = st.session_state['selected_profile_url']

        st.markdown(f'<div><p>Profile URL: <a href="{profile_url}" target="_blank">{profile_url}</a></p></div>', unsafe_allow_html=True)
        
        # Display each post's insight and embed the post
        for post_url, insight in insights.items():
            st.markdown(f'<div class="post-insight">', unsafe_allow_html=True)
            st.markdown(f'<p class="post-url">Post URL: <a href="{post_url}" target="_blank">{post_url}</a></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="insight-text">Insight: {insight}</p>', unsafe_allow_html=True)
            components.iframe(f"{post_url}embed", height=400, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("---")
        
    else:
        st.write("No profile selected.")

if __name__ == "__main__":
    main()
