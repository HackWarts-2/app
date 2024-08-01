import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    st.title("Similar Profiles")


    # trying out instagram post embed
    instagram_url = "https://www.instagram.com/p/C-DzhHLNqDz/embed"
    components.iframe(instagram_url, height=400, width=300)


    # Example profiles, replace with real data as needed
    profiles = [
        {"name": "Profile A", "description": "This is profile A"},
        {"name": "Profile B", "description": "This is profile B"},
        {"name": "Profile C", "description": "This is profile C"},
    ]

    for profile in profiles:
        if st.button(profile['name']):
            st.session_state['selected_profile'] = profile
            # st.experimental_rerun()  # Refresh the app state to ensure session state is updated
            st.switch_page("pages/3_profile_details.py")  # This will navigate to the Profile Details page

if __name__ == "__main__":
    main()
