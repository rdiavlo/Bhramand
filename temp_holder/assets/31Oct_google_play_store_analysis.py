"""
1. Look at the data
2. Clean the data
3. Ask questions
4. Use visuals to answer questions
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format

apps_df = pd.read_csv("data/google play store data/apps.csv")

# print(apps_df.head())
# print(apps_df.tail())

# check for nulls & column types
print(apps_df.shape)
print(apps_df.info())


print("=="*38)
apps_df_cleaned = apps_df
# convert last updated to datetime format and drop unnecessary columns
apps_df_cleaned.loc['Last_Updated'] = pd.to_datetime(apps_df_cleaned['Last_Updated'])
apps_df_cleaned.drop(columns=['Last_Updated', 'Android_Ver'], inplace=True)


# Cleaning nulls [No rating, android version, type][Count: 1477]
print(apps_df.shape[0])
print("The count of nulls pre cleansing is: ", apps_df.isna().values.sum())
apps_df_cleaned = apps_df.dropna()
print("The count of nulls post cleansing is: ", apps_df_cleaned.isna().values.sum())
print(apps_df_cleaned.shape[0])


print("=="*38)
# check for duplicates
print("The count of duplicates pre cleanse is: ", apps_df_cleaned.duplicated().values.sum())
apps_df_cleaned.drop_duplicates(subset=['App', 'Type', 'Price'], inplace=True)
print("The count of duplicates post cleanse is: ", apps_df_cleaned.duplicated().values.sum())
print(apps_df_cleaned.shape[0])

print("=="*38)
# Remove commas from Install column & convert to Int datatype
# Remove dollars and convert Price column to Int datatype
apps_df_cleaned['Installs'] = apps_df_cleaned['Installs'].transform(func=lambda x : x.replace(",", ""))
apps_df_cleaned.Installs = pd.to_numeric(apps_df_cleaned.Installs)
apps_df_cleaned['Price'] = apps_df_cleaned['Price'].astype(str).str.replace('$', "")
apps_df_cleaned['Price'] = pd.to_numeric(apps_df_cleaned['Price'])


# Remove the bad data Outrageous prices --> 'I am rich' App spin-offs
apps_df_cleaned['Price'] = apps_df_cleaned[apps_df_cleaned['Price'] < 250]['Price']



"""
Challenge: Identify which apps are the highest rated. What problem might you encounter if you rely exclusively 
on ratings alone to determine the quality of an app?

Challenge: What's the size in megabytes (MB) of the largest Android apps in the Google Play Store.
Based on the data, do you think there could be a limit in place or can developers make apps as large as they please?

Challenge: Which apps have the highest number of reviews? Are there any paid apps among the top 50?
"""

def dump():
    # Top-rated and largest size apps
    top_rated_apps_df = apps_df_cleaned.sort_values("Rating", ascending=False)
    print(top_rated_apps_df.shape)
    largest_size_apps_df = apps_df_cleaned.sort_values("Size_MBs", ascending=False)
    print(top_rated_apps_df.shape)


    # Plot the app size Vs. downloads [Observed: 20 MB global maxima and sharp decline, 100 MB maxima]
    size_df = apps_df_cleaned.sort_values('Size_MBs')['Size_MBs']
    downloads_df = apps_df_cleaned.sort_values('Installs')['Installs']
    downloads_df = downloads_df.rolling(window=600).mean()
    plt.plot(size_df, downloads_df)
    # plt.show()

    # There is no paid app in Top-10 of playstore
    highest_review_apps_df = apps_df_cleaned.sort_values("Reviews", ascending=False)[['App', 'Reviews', 'Size_MBs', 'Type']].head(10)
    # print(highest_review_apps_df)


# visualize_content_ratings
def visualize_content_ratings():
    content_ratings_df = apps_df_cleaned['Content_Rating']
    content_count_df = content_ratings_df.value_counts()

    fig = px.pie(labels=content_count_df.index,
                 values=content_count_df.values,
                 title="Content Rating",
                 names=content_count_df.index,
                 hole=0.6,
                 )
    fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')

    fig.show()


# Plot the app size Vs. downloads [Observed: 20 MB global maxima and sharp decline, 100 MB maxima]
size_df = apps_df_cleaned.sort_values('Size_MBs')['Size_MBs']
downloads_df = apps_df_cleaned.sort_values('Installs')['Installs']
downloads_df = downloads_df.rolling(window=100).mean()
plt.plot(size_df, downloads_df)
# plt.show()

"""
Questions:

Obj1: Make money
    What is the correlation between genre and installs [o11_df]
    Optimal strategy to make money [Price + Installs]
    Which customer segment to target
    How does reviews and ratings affect installs


Highest money making apps --> Build AI app designer coupled with minions
[Use idea/artifact replication (Espionage)] --> Identify unused potential
"""

# What is the correlation between genre and installs [Select top 500]
# o11_df = apps_df_cleaned[['App', 'Genres', 'Installs']]
# top_100_installs = o11_df.sort_values(by=['Installs'], ascending=False)[:401]
# print(top_100_installs.head(5))
# top_100_installs = top_100_installs['App'].unique()
# print(top_100_installs[:5])


# Add a column called 'Revenue_Estimate' to the DataFrame. This column should hold the price of the app times the
# number of installs. What are the top 10 highest-grossing paid apps according to this estimate? Out of the top 10,
# how many are games?

# apps_df_cleaned['Revenue_Estimate_df'] = apps_df_cleaned['Price'].mul(apps_df_cleaned['Installs'])
# res = apps_df_cleaned.sort_values('Revenue_Estimate_df', ascending=False).head(20)
# print(res[['Revenue_Estimate_df', 'App', 'Reviews', 'Installs', 'Price', 'Genres', 'Category']])


# The number of categories --> 33
# print(apps_df_cleaned['Category'].nunique())
# Number of apps per category
category_count_df = apps_df_cleaned['Category'].value_counts()

# bar_plot = px.bar(x=category_count_df.index, y=category_count_df.values)
# bar_plot.show()


# Get number of installs per category
number_of_installs_df = apps_df_cleaned.groupby('Category').agg({'Installs': pd.Series.sum})
number_of_installs_df.sort_values('Installs', ascending=True, inplace=True)

# h_bar_chart = px.bar(x=number_of_installs_df['Installs'], y=number_of_installs_df.index, orientation='h',
#                      title='Category Popularity')
# h_bar_chart.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
# h_bar_chart.show()


def get_app_count_category_and_install_insights():
    category_count_mod_df = pd.DataFrame(category_count_df.values, index=category_count_df.index, columns=['Count of apps'])
    # print(category_count_mod_df.shape)
    # print(category_count_mod_df.head())
    # print(number_of_installs_df.shape)
    # print(number_of_installs_df.head())

    # join both tables --> To get count of apps Vs. Installs
    merged_df = category_count_mod_df.merge(number_of_installs_df, left_index=True, right_index=True)

    merged_df = merged_df[:20]

    scatter_plot = px.scatter(merged_df, x='Count of apps', y='Installs',title='Category Concentration',
                              size='Count of apps', hover_name=merged_df.index,
                              color='Installs')
    scatter_plot.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                          yaxis_title="Installs",
                          yaxis=dict(type='log'))
    # scatter_plot.show()

    # Plot 'category' Vs. 'average installs per app'
    merged_df['Avg installs per app'] = merged_df['Installs'].div(merged_df['Count of apps'])
    merged_df.sort_values('Avg installs per app', ascending=False, inplace=True)
    print(merged_df.head())
    bar_plot = px.bar(x=merged_df.index, y=merged_df['Avg installs per app'])
    bar_plot.update_layout(xaxis_title='Category', yaxis_title='Avg installs per app')
    # bar_plot.show()


def explore_genres():
    # How many different types of genres are there? Can an app belong to more than one genre?
    # Check what happens when you use .value_counts() on a column with nested values? See if you can work around
    # this problem by using the .split() function and the DataFrame's .stack() method.

    stacked_genres_df = apps_df_cleaned['Genres'].str.split(";", expand=True).stack()
    print(f'We now have a single column with shape: {stacked_genres_df.shape}')
    print("The number of genres: ", len(stacked_genres_df.value_counts()))
    genre_and_number_of_apps_df = stacked_genres_df.value_counts().sort_values(ascending=False)[:16]

    bar_plot = px.bar(genre_and_number_of_apps_df, x=genre_and_number_of_apps_df.index, y=genre_and_number_of_apps_df.values,
                      color=genre_and_number_of_apps_df.values, title="Genre Vs. Count of app installs",
                      color_continuous_scale='Agsunset')

    bar_plot.update_layout(xaxis_title='Genre', yaxis_title='Count of app installs',
                           coloraxis_showscale=False)
    bar_plot.show()


def paid_vs_free_insights():
    # We can group our data first by Category and then by Type. Then we can add up the number of apps per each type.
    # Using as_index=False we push all the data into columns rather than end up with our Categories as the index.


    category_type_df = apps_df_cleaned.groupby(['Category', 'Type'], as_index=False).agg({'App': pd.Series.count})
    category_type_df.sort_values('App', inplace=True)

    category_type_df.sort_values('Type', inplace=True)
    print(category_type_df.head())
    g_bar = px.bar(category_type_df,
                   x='Category',
                   y='App',
                   title='Free vs Paid Apps by Category',
                   color='Type',
                   barmode='group')

    g_bar.update_layout(xaxis_title='Category',
                        yaxis_title='Number of Apps',
                        xaxis={'categoryorder': 'total descending'},
                        yaxis=dict(type='log'))
    g_bar.show()


"""
But this leads to many more questions:

How much should you charge? What are other apps charging in that category?

How much revenue could you make?

And how many downloads are you potentially giving up because your app is paid?
"""

paid_apps_df = apps_df_cleaned[apps_df_cleaned['Type'] == 'Paid']
paid_apps_df = paid_apps_df.groupby('Category', as_index=False)['Price']
print(paid_apps_df.head())

paid_apps_df = paid_apps_df.agg([pd.Series.min, pd.Series.max, pd.Series.mean])
print(paid_apps_df.sort_values('mean', ascending=False)[:5])


print("checkkkkkkkkkkkk")
category_mean_price = paid_apps_df['mean']
print(category_mean_price.head())