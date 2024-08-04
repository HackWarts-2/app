import streamlit as st

def main():
    st.set_page_config(page_title="AppName", page_icon=":house:")
    
    # Sidebar styling
    sidebar_style = """
    <style>
    .sidebar .sidebar-content {
        font-family: 'Arial', sans-serif;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
    }
    .sidebar .sidebar-content h2 {
        color: #ff6b6b;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content p {
        color: #4b4b4b;
        font-size: 16px;
    }
    </style>
    """

    st.markdown(sidebar_style, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<div class='sidebar-content'><h2>AppName</h2>", unsafe_allow_html=True)
        st.markdown("<p>Enhance your Instagram profile with detailed, personalized analysis.</p></div>", unsafe_allow_html=True)

    st.title("AppName")
    st.write("Enhance your Instagram profile with detailed, personalized analysis.")
    
if __name__ == "__main__":
    main()
