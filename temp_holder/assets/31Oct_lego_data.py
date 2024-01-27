import pandas as pd



pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format

print("--"*40)
df = pd.read_csv("data/colors.csv")
print(df.columns)
df.rename(columns={"name": "color"}, inplace=True)
print(df.head())
print(df.shape)

print("--"*40)
colour_df = df.groupby('color')
print("The number of unique colors are: ", df['color'].nunique())
print("Alternate: The number of unique colors are: ", df['is_trans'].value_counts())

print("--"*40)
print("The transparent Vs. non-transparent colors are: ")
transparency_df = df.groupby('is_trans')
print(transparency_df.count())


"""
The sets.csv contains a list of LEGO sets. 
It shows in which year the set was released and the number of parts in the set.

Then try and answer the following questions:
    1. In which year were the first LEGO sets released and what were these sets called?
    2. How many different products did the LEGO company sell in their first year of operation?
    3. What are the top 5 LEGO sets with the most number of parts? 
"""
print("--"*40)
lego_sets_df = pd.read_csv("data/sets.csv")
print(lego_sets_df.head())

print("--"*40)
# 1. In which year were the first LEGO sets released and what were these sets called?
min_year = lego_sets_df["year"].min()
print("The first lego sets were released in: ", min_year)

print("--"*40)
# 2. How many different products did the LEGO company sell in their first year of operation?
year_min = lego_sets_df[lego_sets_df["year"] == 1949].sort_values('num_parts')
print(year_min)

print("--"*40)
# 3. What are the top 5 LEGO sets with the most number of parts?
top_5_num_of_parts = lego_sets_df.sort_values('num_parts', ascending=False)
print(top_5_num_of_parts.head())


import matplotlib.pyplot as plt

print("--"*40)

# ax1 = plt.gca()  # get current axes
# ax2 = ax1.twinx() # Get another axis that shares the same x-axis
#
# # plot number of lego sets published over years
# plt_lego_df= lego_sets_df.groupby("year").count()
# plt_lego_df_x = plt_lego_df.index[:-2]
# plt_lego_df_y = plt_lego_df["set_num"][:-2]
# ax1.plot(plt_lego_df_x, plt_lego_df_y, color='g')
#
# # Calculate the number of different themes by calendar year
# no_of_themes_df = lego_sets_df.groupby('year').agg({'theme_id':pd.Series.nunique})
# no_of_themes_df.rename(columns={'theme_id': 'unique_themes_by_year'}, inplace=True)
# ax2.plot(no_of_themes_df.index[:-2], no_of_themes_df['unique_themes_by_year'][:-2], color='b')
#
# ax1.set_xlabel('Year')
# ax1.set_ylabel('Number of sets', color='g')
# ax2.set_ylabel('Number of themes',  color='b')


# Create a Pandas Series called parts_per_set that has the year as the index and contains the average number
# of parts per LEGO set in that year. Here's what you're looking to create
# parts_per_set = lego_sets_df.groupby('year').agg({'num_parts': pd.Series.mean})
# print(parts_per_set)
#
# plt.scatter(parts_per_set.index[:-2], parts_per_set['num_parts'][:-2])
#
# plt.show()
#
#




print(lego_sets_df.head())
print(lego_sets_df.tail())


theme_count_df = lego_sets_df.groupby('theme_id').count()
print(lego_sets_df['theme_id'].value_counts())


# get the themes
themes_df = pd.read_csv('data/themes.csv')
print(themes_df[themes_df['name'] == 'Star Wars'])


print("--"*40)
# join theme and lego-set tables
# should have same column names
print(themes_df[themes_df['name'] == 'Star Wars'].head())
t_themes_df = lego_sets_df['theme_id'].value_counts()
print(t_themes_df)
print(t_themes_df.index)


df = pd.DataFrame({
    'id': t_themes_df.index,
    'counts': t_themes_df.values
})

print(df.head())
print(df.columns)


merged_df = pd.merge(df, themes_df, on="id")
print(merged_df.head())



plt.figure(figsize=(14,8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel('Nr of Sets', fontsize=14)
plt.xlabel('Theme Name', fontsize=14)
plt.bar(merged_df['name'].head(10), merged_df['counts'].head(10))



plt.show()