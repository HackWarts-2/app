import streamlit as st

def main():
    st.set_page_config(page_title="Profile Details", page_icon=":bust_in_silhouette:")
    st.title("Profile Details")

    if 'selected_profile' in st.session_state:
        profile = st.session_state['selected_profile']
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Description:** {profile['description']}")
    else:
        st.write("No profile selected.")

if __name__ == "__main__":
    main()
