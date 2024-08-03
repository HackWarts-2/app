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
        background-color: #ff5733;
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
</style>
"""
def format_number(number):
    """Format a number with commas as thousands separators."""
    return f"{number:,}"

# Example usage
formatted_1000 = format_number(1000)       # Outputs '1,000'
formatted_100000 = format_number(100000)   # Outputs '100,000'

print(formatted_1000)
print(formatted_100000)

def main():


    
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Navbar
    st.markdown('<div class="navbar">Similar Profiles</div>', unsafe_allow_html=True)
  
    # Access the similar_profiles_data from session state
    if 'similar_profiles_data' in st.session_state:
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
                st.markdown(f'<div class="profile-details">', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-username">{profile["username"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-followers">Followers: {format_number(profile["followersCount"])}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="profile-bio">{profile["biography"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p><a href="{profile["inputUrl"]}" class="visit-profile" target="_blank">Visit Profile</a></p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("---")
    else:
        st.write("No similar profiles found. Please go back and try again.")

if __name__ == "__main__":
    main()
