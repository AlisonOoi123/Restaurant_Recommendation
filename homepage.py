import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(layout='centered', initial_sidebar_state='expanded')

# Sidebar logo
st.sidebar.image('Data/App_icon.png')

# Main content
image = Image.open('Data/Food.jpg')
st.image(image, use_column_width=True)

st.title("Discover the Best Places to Eat in Your Town")

st.markdown("Welcome to our app! Powered by data from TripAdvisor, we curate recommendations from 20 cities across New York, New Jersey, California, Texas, and Washington. Find the top 10 restaurants similar to your favorites.")

st.markdown("Leveraging Natural Language Processing and Content-Based Recommender Systems, we prioritize user comments to deliver personalized suggestions. Satisfy your cravings with ease!")

# Sidebar options
option = st.sidebar.selectbox(
    'Select a City',
    ('New York', 'Los Angeles', 'San Francisco', 'Houston', 'Seattle', 'Jersey City', 'Austin', 'San Diego', 'Washington DC', 'Chicago')
)

# Depending on the city selected, show relevant information
if option == 'New York':
    st.markdown("### New York City")
    st.markdown("New York City is known for its diverse culinary scene. From classic New York pizza to Michelin-starred restaurants, there's something for everyone.")
    st.markdown("Check out our recommendations for the best eateries in the Big Apple!")

elif option == 'Los Angeles':
    st.markdown("### Los Angeles")
    st.markdown("Los Angeles offers a wide range of dining experiences, from trendy rooftop bars to hidden gems in ethnic neighborhoods.")
    st.markdown("Explore our top picks for dining destinations in the City of Angels!")

# Add more elif blocks for other cities...

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed by YourCompany")
st.sidebar.markdown("[GitHub](https://github.com/YourGitHub)")

