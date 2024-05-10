import streamlit as st
import seaborn as sns
import itertools
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.sidebar.image('Data/App_icon.png')

st.markdown("""
# Welcome to our restaurant insights page!
Discover fascinating trends and data-driven analysis of the culinary landscape. From popular cuisine types to the best states and cities for food lovers, we've got you covered.
""")
st.text("")

df = pd.read_csv("./Data/TripAdvisor_RestauarantRecommendation.csv")
df = df.drop(['Contact Number', 'Trip_advisor Url',
       'Menu'],axis=1)
df = df.drop([1744,2866])
df = df.reset_index(drop=True)
df.Comments = df.Comments.fillna('')
df.Type = df.Type.fillna(df.Type.value_counts().index[0])

col1, col2 = st.columns(2)

types = []
for i in range(len(df)):
    if type(df.Type[i]) == str:
        types.append(df.Type[i].split(",")) 
flat_list = list(itertools.chain(*types))
series = pd.Series(flat_list)
fig, ax = plt.subplots()
ax = pd.Series(series).value_counts()[:10].plot(kind='pie', shadow=True,  cmap=plt.get_cmap('Spectral'))
ax.set_ylabel('Cuisine Types')


with col2:
           
    st.markdown("""
    ### 10 Most Popular Types of Cuisines
    Ever wondered what cuisines people are loving the most? Dive into our interactive visualization to explore the top 10 most popular types of cuisines based on our data. From Italian to Japanese, uncover the culinary delights that are capturing diners' hearts.
    """)
    st.pyplot(fig)

### Seperating State, City and Zip Code from Location Column
df['State'] = [i.split(",")[-1].split(" ")[1] for i in df.Location]
df['ZipCode'] = [i.split(",")[-1].split(" ")[-1] for i in df.Location]
df['City'] = [",".join(i.split(",")[:-1]) for i in df.Location]
df = df.drop(['Location'],axis=1)
df = df.drop(df[df.State==''].index[0])
df.State.value_counts()


# ax = df.State.value_counts().plot(kind="bar", color="Purple",  figsize=(10,5))
fig, ax = plt.subplots()
ax = sns.barplot(x=df['State'].value_counts().index, y = df['State'].value_counts(),palette="rocket")
ax.set_ylabel('No of Restaurants')
ax.set_xlabel('State')
for i in ['top','right']:
    ax.spines[i].set_visible(False)
plt.gcf().set_size_inches(7, 5)

# Set the background color
ax.set_facecolor('#f0f0f0')  # Change '#f0f0f0' to the color you prefer

with col1:
    st.markdown("""
    ## No of Restaurants per State
    Curious about which states boast the highest number of restaurants? Our bar chart breaks down the restaurant scene across different states, giving you insights into where culinary diversity thrives.
    """)
    st.pyplot(fig)


### Converting the string values to float/int values
df['Reviews'] = [float(i.split(" ")[0]) for i in df.Reviews]
df['No of Reviews'] = [int(i.split(" ")[0].replace(",","")) for i in df['No of Reviews']]
### Weighted Ratings - No of Reviewers * Average Ratings
df['weighted_ratings'] = df.Reviews*df['No of Reviews']
labels = df.State.unique().flatten()
average_vote_share_list = [df[df.State==i].weighted_ratings.max() for i in labels]
avg_wt_ratings = pd.DataFrame({'State':labels, 'Weighted Average Ratings': average_vote_share_list})

st.text("")
col1, col2, col3 = st.columns(3)
plot = sns.catplot(x='State', y="Weighted Average Ratings", kind="bar", data=avg_wt_ratings, palette="PuOr")
plt.gcf().set_size_inches(7, 7)

with col1:
    st.markdown("""
    ## State with the Best Restaurant
    Delve into our analysis of the state with the best restaurant. We've calculated weighted average ratings to determine which state offers the ultimate dining experience, combining both quality and quantity.
    """)
    st.pyplot(plot)

labels = df.State.unique().flatten()
total_vote_share_list = [df[df.State==i].weighted_ratings.sum() for i in labels]
total_wt_ratings = pd.DataFrame({'State':labels, 'Total Weighted Ratings': total_vote_share_list})
plot = sns.catplot(x='State', y="Total Weighted Ratings", kind="bar", data=total_wt_ratings, palette="mako")
plt.gcf().set_size_inches(7, 7)

with col2:
    st.markdown("""
    ## Best State For Food
    Looking for the ultimate foodie destination? Explore our findings on the best state for food based on total weighted ratings. Whether you're craving gourmet cuisine or down-home cooking, this state promises a gastronomic adventure.
    """)
    st.text("")

    st.pyplot(plot)



labels = df.City.unique().flatten()
total_vote_share_list = [df[df.City==i].weighted_ratings.sum() for i in labels]
total_wt_ratings = pd.DataFrame({'City':labels, 'Total Weighted Ratings': total_vote_share_list})
total_wt_ratings = total_wt_ratings.sort_values(by=['Total Weighted Ratings'],ascending=False).head(5)
plot = sns.catplot(x='City', y="Total Weighted Ratings", kind="bar", data=total_wt_ratings, palette="flare")
plt.gcf().set_size_inches(7, 7)
with col3:
    st.markdown("""
    ## Top 5 Cities For Food
    Discover the top 5 cities that are culinary hotspots. Our analysis reveals the cities where food lovers can indulge in the finest dining experiences, from bustling metropolises to charming culinary gems.
    """)
    st.pyplot(plot)
