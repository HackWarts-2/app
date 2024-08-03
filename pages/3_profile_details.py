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
        background-color: #ff5733;
        padding: 1rem;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .profile-details-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .post-insight {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.05);
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
    
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Navbar
    st.markdown('<div class="navbar">Profile Details</div>', unsafe_allow_html=True)

    # Access the selected profile insights and URL from session state
    if 'selected_profile_insights' in st.session_state and 'selected_profile_url' in st.session_state:
        insights = st.session_state['selected_profile_insights']
        profile_url = st.session_state['selected_profile_url']

        st.markdown(f'<div class="profile-details-container"><p>Profile URL: <a href="{profile_url}" target="_blank">{profile_url}</a></p></div>', unsafe_allow_html=True)
        
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
