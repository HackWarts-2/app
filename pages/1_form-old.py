import streamlit as st
from utils import userData, getInsights

def main():
    st.set_page_config(page_title="Form", page_icon=":memo:")
    st.title("Form")

    # Input fields for username and search query
    username = st.text_input("Username")
    search_query = st.text_input("Search Query")

    # Button to trigger the fetch action
    if st.button("Fetch"):
        if username and search_query:
            with st.spinner("Fetching data..."):
                user_data = userData(username)
                insights = getInsights(user_data, search_query)
                st.session_state['insights'] = insights
            st.success("Data fetched successfully!")
            st.switch_page("pages/2_similar_profiles.py")
        else:
            st.error("Please provide both username and search query")


if __name__ == "__main__":
    main()
