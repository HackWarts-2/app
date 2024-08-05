import streamlit as st
import requests
from PIL import Image
from io import BytesIO

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
    .profile-image {
        border-radius: 50%;
        margin-right: 1rem;
        width: 100px;
        height: 100px;
    }
    .stMarkdown {
        color: #E4405F; /* Instagram red */
    }
    .profile-details {
        flex: 1;
    }
    .profile-username {
        font-size: 1.5rem;
        font-weight: bold;
        color: #833AB4; /* Instagram gradient color */
    }
    .profile-followers {
        font-size: 1.2rem;
        color: #FD1D1D; /* Instagram gradient color */
    }
    .profile-bio {
        font-size: 1rem;
        color: #5851DB; /* Instagram gradient color */
    }
    .visit-profile {
        color: #E1306C; /* Instagram gradient color */
        font-weight: bold;
    }
    .sidebar-font{
                color:black}
</style>
"""

def format_number(number):
    """Format a number with commas as thousands separators."""
    return f"{number:,}"

from utils import getInsightsForProfile

# Initialize the session state keys if they do not exist
if 'user_data_response' not in st.session_state:
    st.session_state['user_data_response'] = None

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    
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
    st.markdown('<div class="navbar">Similar Profiles</div>', unsafe_allow_html=True)
  
    # Access the similar_profiles_data from session state
    if 'similar_profiles_data' in st.session_state and st.session_state['similar_profiles_data']:
        similar_profiles_data = st.session_state['similar_profiles_data']

        # Display the similar profiles
        for profile in similar_profiles_data:
            col1, col2 = st.columns([1, 3])
            with col1:
                try:
                    response = requests.get(profile['profilePicUrl'])
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, width=100, use_column_width='always', caption=profile.get('username', 'Profile Picture'))
                    else:
                        st.write("Image could not be loaded")
                except Exception as e:
                    st.write(f"Error loading image: {e}")
            with col2:
                st.markdown('<div class="profile-details">', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-username">{profile["username"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-followers">Followers: {format_number(profile["followersCount"])}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-bio">{profile["biography"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><a href="{profile["inputUrl"]}" class="visit-profile" target="_blank">Visit Profile</a></p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
           
            # Get Insights button
            if st.button(f"Get Insights for {profile['username']}", key=profile['username']):
                if st.session_state['user_data_response']:
                    print("User Data Response:", st.session_state['user_data_response'])
                    # Generate insights
                    insights = getInsightsForProfile(st.session_state['user_data_response'], profile['inputUrl'])
                    
                    # Save the insights and selected profile to session state
                    st.session_state['selected_profile_insights'] = insights
                    st.session_state['selected_profile_url'] = profile['inputUrl']
                    
                    # Redirect to profile details page
                    st.switch_page("pages/3_profile_details.py")
                elif st.session_state.get('user_data_fetching', False):
                    st.warning("User data is still being fetched. Please try again in a few seconds.")
                else:
                    st.error("Failed to fetch user data.")
            if st.button(f"Ask anything from {profile['username']}", key=f"chat{profile['username']}"):
                st.session_state['selected_username']=profile['username']
                st.switch_page("pages/7_UserSpecificBot.py")      
            st.write("---")
    else:
        st.write("No similar profiles found. Please go back and try again.")

if __name__ == "__main__":
    main()
