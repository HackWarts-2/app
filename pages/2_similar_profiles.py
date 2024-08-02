import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    st.title("Similar Profiles")

    # Access the similar_profiles_data from session state
    if 'similar_profiles_data' in st.session_state:
        similar_profiles_data = st.session_state['similar_profiles_data']

        # Display the similar profiles
        for profile in similar_profiles_data:
            st.write(f"**Username:** {profile['username']}")
            st.write(f"**Followers:** {profile['followersCount']}")
            st.write(f"**Biography:** {profile['biography']}")
            
            # Attempt to display the profile image
            try:
                # Make a request to fetch the image content
                response = requests.get(profile['profilePicUrl'])
                if response.status_code == 200:
                    # If the request is successful, load the image using PIL
                    image = Image.open(BytesIO(response.content))
                    st.image(image, width=100)
                else:
                    st.write("Image could not be loaded")
            except Exception as e:
                st.write(f"Error loading image: {e}")

            st.markdown(f"[Visit Profile]({profile['inputUrl']})")
            st.write("---")
    else:
        st.write("No similar profiles found. Please go back and try again.")

if __name__ == "__main__":
    main()
