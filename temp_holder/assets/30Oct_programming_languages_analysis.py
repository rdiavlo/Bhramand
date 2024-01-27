import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format

df = pd.read_csv("programming_languages.csv", header=0, names=["Date", "Tag", "Posts"])

# print(df.describe())
print(df.head())
print(df.shape)
print(df.count())

clean_df = df.isna()
clean_df.dropna(inplace=True)

print(clean_df.shape)

res = df.groupby('Tag')
print("\nThe number of posts in a given language are: ")
print(res['Posts'].count())
print("\nThe languages with the maximum posts are: ")
print(res['Posts'].sum().sort_values(ascending=False))


# Data cleaning
print(df.head())
date_row = df['Date'][0]
print(date_row)
print(type(date_row))

df['Date'] = pd.to_datetime(df['Date'])
print(df.head())


# Pivot the dataframe
test_df = pd.DataFrame({'Age': ['Young', 'Young', 'Young', 'Young', 'Old', 'Old', 'Old', 'Old'],
                        'Actor': ['Jack', 'Arnold', 'Keanu', 'Sylvester', 'Jack', 'Arnold', 'Keanu', 'Sylvester'],
                        'Power': [100, 80, 25, 50, 99, 75, 5, 30]})
print(test_df)

pivoted_df = test_df.pivot(index='Age', columns='Actor', values='Power')
print(pivoted_df)

# reshape df
reshaped_df = df.pivot(index='Date', columns='Tag', values='Posts')
print(reshaped_df.head())

# fill nulls
reshaped_df.fillna(0, inplace=True)
print(reshaped_df.head())

print("Check for null values:", reshaped_df.isna().values.any())

roll_df = reshaped_df.rolling(window=12).mean()

# # plot popularity of programming language --> python
plt.figure(figsize=(8,5))
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
plt.xlabel('Date', fontsize=7)
plt.ylabel('Number of Posts', fontsize=7)
plt.ylim(0, 35000)
for column in reshaped_df.columns:
    x_data = reshaped_df.index
    y_1_data = reshaped_df[column]
    # plt.plot(x_data, y_1_data,
    #          linewidth=1, label=reshaped_df[column].name)

    plt.plot(roll_df.index, roll_df[column],
             linewidth=1, label=roll_df[column].name)

plt.legend()
plt.show()