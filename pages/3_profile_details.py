import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Profile Details", page_icon=":bust_in_silhouette:")
    st.title("Profile Details")

    # Access the selected profile insights and URL from session state
    if 'selected_profile_insights' in st.session_state and 'selected_profile_url' in st.session_state:
        insights = st.session_state['selected_profile_insights']
        profile_url = st.session_state['selected_profile_url']

        st.write(f"**Profile URL:** {profile_url}")
        
        # Display each post's insight and embed the post
        for post_url, insight in insights.items():
            st.write(f"**Post URL:** {post_url}")
            st.write(f"**Insight:** {insight}")
            components.iframe(f"{post_url}embed", height=400, width=300)
            st.write("---")
    else:
        st.write("No profile selected.")

if __name__ == "__main__":
    main()
