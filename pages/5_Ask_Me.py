import streamlit as st

# Define category options
category_options = ["Beauty & Skincare", "Fashion", "Food & Drink", "Health & Fitness",
                "Travel","Lifestyle", "Photography","Art","Technology & Gadgets","Business & Finance",
                "Entertainment","Education & Learning","Automotive","Pets & Animals","Home","Garden","Environmental & Social Issues",
                "Gaming","Events & Parties", "Books & Literature", "Miscellaneous"
                    
                    ]

def main():
    # Initialize session state
    if 'details_entered' not in st.session_state:
        st.session_state.details_entered = False

    # Check if details_entered exists and is True
    if not st.session_state.details_entered:
        st.text_input("Insta Username (optional)")
        
        # Use st.selectbox for the category dropdown
        category = st.selectbox("Category", options=category_options)
        st.session_state.category = category
    else:
        st.text_input("Instagram Username (optional)")

    # Optionally, you can provide a button to set details_entered to True for testing
    if st.button("Enter Details"):
        st.session_state.details_entered = True

if __name__ == "__main__":
    main()
