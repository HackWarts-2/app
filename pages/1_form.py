import streamlit as st
import requests

# Categories and subcategories
categories = {
    "Beauty & Skincare": [
        "Skincare", "Makeup", "Haircare", "Beauty Tips", "Nail Art",
        "Cosmetic Reviews", "Natural/Organic Beauty",
    ],
    "Fashion": [
        "Fashion Blogger", "Personal Style", "Street Style", "Luxury Fashion",
         "Footwear",
        "Accessories & Jewelry"
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
    "Photography & Art": [
        "Photography", "Digital Art", "Painting & Drawing", "Street Photography",
        "Portrait Photography", "Nature Photography", "Abstract Art", "Calligraphy",
        "Tattoo Art", "Graphic Design"
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
    "Home & Garden": [
        "Interior Design", "Home Renovation", "Gardening Tips", 
        "Home Decor", "Real Estate",
        "Outdoor Living",
    ],
   "Religion": [
        "Christian Influencer", "Muslim Influencer", "Jewish Influencer"
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
            .stButton>button {
                background-color: #E1306C; /* Instagram pink */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                border: 1px solid #E1306C; /* Instagram pink */
                background-color: #F7F7F7;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            .stSelectbox>div>div>select {
                border: 1px solid #E1306C; /* Instagram pink */
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
                color: #E1306C; /* Instagram pink */
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Form")

    # Instagram username input (optional)
    instagram_username = st.text_input("Instagram Username (Optional)")

    # Category selection
    category = st.selectbox("Category", options=list(categories.keys()) + ["Blogger"])

    if category == "Blogger":
        all_subcategories = ["None"] + [sub for subs in categories.values() for sub in subs]
    else:
        all_subcategories = ["None"] + categories.get(category, []) + ["Other"]
    
    subcategory = st.selectbox("Subcategory (Optional)", options=all_subcategories)
    
    # If 'Other' is selected, provide an additional input field
    if subcategory == "Other":
        other_subcategory = st.text_input("Please specify the subcategory")
    else:
        other_subcategory = None

    # City input (optional)
    city = st.text_input("City (Optional)")

    # Country input (optional)
    country = st.text_input("Country (Optional)")

    # Handle form submission
    if st.button("Submit"):
        # Prepare the data for the request
        form_data = {
            "instagram_username": instagram_username,
            "category": category,
            "subcategory": subcategory,
            "other_subcategory": other_subcategory,
            "city": city,
            "country": country
        }

        # Send data to the external API
        api_url = "https://example.com/api/endpoint"  # Replace with your API URL
        response = requests.post(api_url, json=form_data)

        if response.status_code == 200:
            # Save form data to session state
            st.session_state.form_data = form_data

           
            st.write("Submitted")

          
           
        else:
            st.error("Failed to submit data. Please try again later.")

if __name__ == "__main__":
    main()
