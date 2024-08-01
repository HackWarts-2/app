import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Similar Profiles", page_icon=":busts_in_silhouette:")
    st.title("Similar Profiles")

    # trying out instagram post embed
    instagram_url = "https://www.instagram.com/p/C-DzhHLNqDz/embed"
    components.iframe(instagram_url, height=400, width=300)

    # Check if insights are available in session state
    if 'insights' in st.session_state:
        insights = st.session_state['insights']
        st.write("Insights received from the form:")
        st.json(insights)
    else:
        st.write("No insights available. Please go back to the form page and submit your query.")

    # Example profiles, replace with real data as needed
    profiles = [
        {"name": "Profile A", "description": "This is profile A"},
        {"name": "Profile B", "description": "This is profile B"},
        {"name": "Profile C", "description": "This is profile C"},
    ]

    for profile in profiles:
        if st.button(profile['name']):
            st.session_state['selected_profile'] = profile
            st.switch_page("pages/3_profile_details.py")


if __name__ == "__main__":
    main()
