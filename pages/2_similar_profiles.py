import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from utils import getInsightsForProfile

# Initialize the session state keys if they do not exist
if 'user_data_response' not in st.session_state:
    st.session_state['user_data_response'] = None

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    st.title("Similar Profiles")

    # Access the similar_profiles_data from session state
    if st.session_state['similar_profiles_data']:
        similar_profiles_data = st.session_state['similar_profiles_data']

        # Display the similar profiles
        for profile in similar_profiles_data:
            st.write(f"**Username:** {profile['username']}")
            st.write(f"**Followers:** {profile['followersCount']}")
            st.write(f"**Biography:** {profile['biography']}")
            
            # Display the profile image
            try:
                response = requests.get(profile['profilePicUrl'])
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    st.image(image, width=100)
                else:
                    st.write("Image could not be loaded")
            except Exception as e:
                st.write(f"Error loading image: {e}")

            st.markdown(f"[Visit Profile]({profile['inputUrl']})")

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
                elif st.session_state['user_data_fetching']:
                    st.warning("User data is still being fetched. Please try again in a few seconds.")
                else:
                    st.error("Failed to fetch user data.")
            st.write("---")
    else:
        st.write("No similar profiles found. Please go back and try again.")

if __name__ == "__main__":
    main()
