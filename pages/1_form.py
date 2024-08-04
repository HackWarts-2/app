import streamlit as st
import requests
import json
from utils import scrape_instagram_similar_profiles, userData
import threading

# Initialize the session state keys if they do not exist
if 'similar_profiles_data' not in st.session_state:
    st.session_state['similar_profiles_data'] = None

if 'user_data_response' not in st.session_state:
    st.session_state['user_data_response'] = None

if 'user_data_fetching' not in st.session_state:
    st.session_state['user_data_fetching'] = False

def remove_none_string(query):
    if "None" in query:
        return query.replace("None", "")
    return query
# Categories and subcategories
categories = {
    "Beauty & Skincare": [
        "Skincare", "Makeup", "Haircare", "Beauty Tips", "Nail Art",
        "Cosmetic Reviews", "Natural/Organic Beauty",
    ],
    "Fashion": [
        "Fashion Blogger", "Personal Style", "Street Style", "Luxury Fashion",
        "Footwear", "Accessories & Jewelry"
    ],
    "Food & Drink": [
        "Food Blogger", "Recipe Sharing", "Food Reviews", "Restaurants & Cafes",
        "Street Food", "Healthy Eating", "Vegan/Vegetarian", "Desserts" ,"Cakes","Cookies","Brownies",
        "Beverages","Coffee","Tea", "Food Photography"
    ],
    "Health & Fitness": [
        "Fitness Coach", "Yoga", "Nutritionist/Dietitian", "Weight Loss",
        "Bodybuilding", "Mental Health & Wellness", "Home Workouts"
    ],
    "Travel": [
        "Travel Blogger", "Adventure Travel", 
        "Solo Travel", "Travel Photography",  "Travel Tips & Hacks",
        "Road Trips", "Local Guides"
    ],
    "Lifestyle": [
        "Daily Life", "Home & Living", "Organization & Productivity", 
        "DIY & Crafts", "Sustainable Living", "Family & Parenting","Relationship Advice"
    ],
    "Photography": [
        "Photography",  "Street Photography",  "Portrait Photography", "Nature Photography"
    ],
    "Art": [
        "Digital Art",  "Painting & Drawing",  "Abstract Art", "Calligraphy", "Tattoo Art", "Graphic Design"
    ],
    "Technology & Gadgets": [
        "Tech Reviews", "Unboxing & Product Demos", "App Reviews", "Gaming",
        "Coding & Programming", "AI & Machine Learning", "Digital Marketing", "Cryptocurrency",
        "Smart Home Gadgets", "Virtual Reality"
    ],
    "Business & Finance": [
        "Entrepreneurship", "Business Strategy", "Finance & Investment", "Real Estate",
        "Personal Finance", "Startups & Innovation", "E-commerce", "Stock Market",
        "Freelancing & Side Hustles", "Leadership & Management"
    ],
    "Entertainment": [
        "Musician/Band", "Actor/Actress", "Comedian", "Movies & TV Shows",
        "Celebrity News", "Book Reviews", "Podcasts", "Event Coverage",
        "Stand-up Comedy", "Live Performances"
    ],
    "Education & Learning": [
        "Online Courses", "Language Learning", "Study Tips", "Educational Content",
        "Science Communication", "History & Culture", "DIY Learning", "Career Advice",
        "Teaching & Tutoring", "Skill Development"
    ],
    "Automotive": [
        "Car Reviews", "Luxury Cars", "Motorcycles",
        "Racing","Electric Vehicles",
        "Car Photography"
    ],
    "Pets & Animals": [
        "Pet Blogger",  "Cat Lovers",  "Wildlife",
        "Pet Products Reviews", "Animal Rescue", "Pet Photography", "Veterinary Advice",
        "Pet Fashion"
    ],
    "Home": [
        "Interior Design", 
        "Home Renovation", 
        "Home Decor", 
        "Real Estate"
    ],
    "Garden": [
        "Gardening Tips", 
        "Outdoor Living"
    ],
    "Environmental & Social Issues": [
        "Environmental Activism", "Climate Change Awareness", 
        "Human Rights Advocacy", "Social Justice", "Animal Rights", "Gender Equality",
       "Non-Profit Organizations"
    ],
    "Gaming": [
        "Game Reviews", "Esports", "Live Streaming", "Gaming News", "Game Development",
        "Mobile Gaming", 
    ],
    "Events & Parties": [
        "Event Planning", "Wedding Planning", "Party Decorations", "Corporate Events",
        "Festival Coverage", "Concerts & Shows", "Event Photography", "Catering",
        "Wedding Photography", "Venue Styling"
    ],
    "Books & Literature": [
        "Book Reviews", "Book Recommendations", "Writing Tips",
        "Poetry", "Book Clubs",  "Self-Publishing", "Fiction & Non-Fiction",
        "Book Photography"
    ],
    "Miscellaneous": [
        "Memes & Humor", "History & Culture",
        "Paranormal", "Conspiracy Theories", 
        "Board Games & Puzzles", "Collectibles & Hobbies"
    ]
}

# Account types
account_types = [
    "Personal Account", "Influencer", "Blogger/Content Creator", "Small Business",
    "Home Business", "Brand/Corporate", "Public Figure/Celebrity", "Artist/Musician/Performer",
    "Photographer", "Fitness Trainer/Coach",
    "E-commerce", "Educational Account", "Travel", "Pet Account", "Entertainment", 
]

def main():
    st.set_page_config(page_title="Form", page_icon=":memo:")

    # Custom CSS for Instagram theme
    st.markdown("""
         <style>
    .reportview-container {
        background-color: #F7F7F7;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .navbar {
        background-color: #8a49a1;
        padding: 1rem;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #e56969;  
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:active {
        background-color: grey;
        color: white;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border: 1px solid #c1888b;
        background-color: #F7F7F7;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stSelectbox>div>div>select {
        border: 1px solid #c1888b;
        background-color: #F7F7F7;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
    }
    .stTitle, .stHeader, .stSubheader {
        color: #405DE6; /* Instagram blue */
    }
    .stText {
        color: #8A3AB9; /* Instagram purple */
    }
    .stMarkdown {
        color: #E4405F; /* Instagram red */
    }
    .stAlert {
        background-color: #F5F5F5;
    }
    .css-1v3fvcr {
        color: #c1888b;  
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="navbar">User Details</div>', unsafe_allow_html=True)

    # Instagram username input (optional)
    instagram_username = st.text_input("Instagram Username (Optional)")

    # Category selection
    category = st.selectbox("Category", options=list(categories.keys()))

    all_subcategories = ["None"] + categories.get(category, []) + ["Other"]
    
    subcategory = st.selectbox("Subcategory (Optional)", options=all_subcategories)
    
    # If 'Other' is selected, provide an additional input field
    if subcategory == "Other":
        other_subcategory = st.text_input("Please specify the subcategory")
    else:
        other_subcategory = None

    # Account type selection
    account_type = st.selectbox("Account Type", options=account_types)

    # City input (optional)
    city = st.text_input("City (Optional)")

    # Country input (optional)
    country = st.text_input("Country (Optional)")

    # Handle form submission
    if st.button("Done"):
       with st.spinner("Fetching Profiles That Match Your Input......"):
        # Prepare the data for the request
        form_data = {
            "instagram_username": instagram_username,
            "category": category,
            "subcategory": subcategory,
            "other_subcategory": other_subcategory,
            "account_type": account_type,  # Add account type to the form data
            "city": city,
            "country": country
        }

        # Construct the query string
        query_parts = []
        query_parts.append(category) 
        st.session_state.category = category
        # Use the other_subcategory if specified, otherwise use the subcategory
        if other_subcategory:
            query_parts.append(other_subcategory)
            st.session_state.sub_category = other_subcategory
        else:
            query_parts.append(subcategory)
            st.session_state.sub_category = subcategory

        # Add the account type
        query_parts.append(account_type)
        st.session_state.account_type = account_type
        # Add the city and/or country if specified
        if city:
            query_parts.append(city)
            st.session_state.city = city
        if country:
            query_parts.append(country)
            st.session_state.country = country
        
        # Join the parts into a single query string
        query_string = " ".join(query_parts)
        print("Generated Query:", query_string)
        query_string = remove_none_string(query_string)
        # Call the scrape_instagram_similar_profiles function
       # similar_profiles_data = scrape_instagram_similar_profiles(query_string)
        st.session_state['query'] = query_string
        # Save the similar_profiles_data to session state
       # st.session_state['similar_profiles_data'] = json.loads(similar_profiles_data)

        # Set the user_data_fetching flag to True
        st.session_state['user_data_fetching'] = True

        # Run the userData function synchronously
        user_data_response = userData(instagram_username)
        st.session_state['user_data_response'] = user_data_response
        st.session_state['user_data_fetching'] = False

        print("User Data Response:", user_data_response)
        st.session_state.details_entered = True

        # Navigate to the similar profiles page
        st.switch_page("pages/2_similar_profiles.py")

if __name__ == "__main__":
    main()
