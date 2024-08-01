import streamlit as st

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    st.title("Similar Profiles")

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
