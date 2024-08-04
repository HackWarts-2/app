import streamlit as st

def main():
# Initialize session state
    if 'details_entered' not in st.session_state:
        st.session_state.details_entered = False

# Check if details_entered exists and is True
    if st.session_state.details_entered==False:
        st.text_input("Insta Username (optional)")
        st.text_input("Category")
    else:    
        st.text_input("Instagram Username (optional)")

# Optionally, you can provide a button to set details_entered to True for testing
    
if __name__ == "__main__":
    main()
