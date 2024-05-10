import streamlit as st
import seaborn as sns
import itertools
import pandas as pd
import matplotlib.pyplot as plt

# Set page layout and sidebar
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Main page title
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #ff9900;
        padding-top: 30px;
        padding-bottom: 30px;
    }
    </style>
    <div class="main-title">Welcome to our restaurant insights page!</div>
    """,
    unsafe_allow_html=True,
)

# Load data
df = pd.read_csv("./Data/TripAdvisor_RestauarantRecommendation.csv")
df = df.drop(['Contact Number', 'Trip_advisor Url', 'Menu'], axis=1)
df = df.drop([1744, 2866])
df = df.reset_index(drop=True)
df.Comments = df.Comments.fillna('')
df.Type = df.Type.fillna(df.Type.value_counts().index[0])

# Sidebar and main content layout
col1, col2 = st.columns([1, 2])

# Visualization for popular cuisine types
types = list(itertools.chain(*[t.split(",") for t in df.Type if isinstance(t, str)]))
types_counts = pd.Series(types).value_counts()[:10]
fig, ax = plt.subplots()
types_counts.plot(kind='pie', shadow=True, cmap=plt.get_cmap('Spectral'), ax=ax)

ax.set_ylabel('')  # Remove y-label
ax.set_title('10 Most Popular Types of Cuisines', color='#ff9900')
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
col2.pyplot(fig)

# Visualization for number of restaurants per state
df['State'] = [i.split(",")[-1].split(" ")[1] for i in df.Location]
df = df.drop(df[df.State == ''].index[0])
state_counts = df['State'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=state_counts.index, y=state_counts, palette="Set2", ax=ax)

ax.set_ylabel('No of Restaurants', color='#333333')
ax.set_xlabel('State', color='#333333')
ax.set_title('No of Restaurants per State', color='#ff9900')
plt.xticks(rotation=45, color='#333333')
plt.tight_layout()
col1.pyplot(fig)

# State with the best restaurant
df['Reviews'] = [float(review.split(" ")[0]) for review in df.Reviews]
df['No of Reviews'] = [int(reviews.split(" ")[0].replace(",", "")) for reviews in df['No of Reviews']]
df['weighted_ratings'] = df.Reviews * df['No of Reviews']
state_avg_ratings = df.groupby('State')['weighted_ratings'].max().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='State', y="weighted_ratings", data=state_avg_ratings, palette="YlGnBu", ax=ax)

ax.set_ylabel('Weighted Average Ratings', color='#333333')
ax.set_xlabel('State', color='#333333')
ax.set_title('State with the Best Restaurant', color='#ff9900')
plt.xticks(rotation=45, color='#333333')
plt.tight_layout()
col1.pyplot(fig)

# Best state for food
state_total_ratings = df.groupby('State')['weighted_ratings'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='State', y="weighted_ratings", data=state_total_ratings, palette="BuPu", ax=ax)

ax.set_ylabel('Total Weighted Ratings', color='#333333')
ax.set_xlabel('State', color='#333333')
ax.set_title('Best State For Food', color='#ff9900')
plt.xticks(rotation=45, color='#333333')
plt.tight_layout()
col2.pyplot(fig)

# Top 5 cities for food
df['City'] = [",".join(i.split(",")[:-1]) for i in df.Location]
city_total_ratings = df.groupby('City')['weighted_ratings'].sum().reset_index().sort_values(by='weighted_ratings', ascending=False).head(5)
fig, ax = plt.subplots()
sns.barplot(x='City', y="weighted_ratings", data=city_total_ratings, palette="viridis", ax=ax)

ax.set_ylabel('Total Weighted Ratings', color='#333333')
ax.set_xlabel('City', color='#333333')
ax.set_title('Top 5 Cities For Food', color='#ff9900')
plt.xticks(rotation=45, color='#333333')
plt.tight_layout()
col2.pyplot(fig)
