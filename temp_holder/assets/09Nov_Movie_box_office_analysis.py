import pandas as pd

raw_df = pd.read_csv("data/movie box office/cost_revenue_dirty.csv")

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format

print(raw_df.shape)
print(raw_df.info())
print(raw_df.describe())
print(raw_df.head())
print(raw_df.tail())


"""
1. Remove/Replace nulls [Remove][Can see from info that there is no nulls][Double check]
2. Remove duplicates
3. Data type conversions
    -- release date --> date
    -- USD_Worldwide_Gross --> float
    -- USD_Production_Budget --> float
"""

#  convert df
# convert release date --> date
import datetime
def convert_str_to_date(inp):
    r = datetime.datetime.strptime(inp, '%m/%d/%Y')
    return r

print("=="*50)
clean_df = raw_df
clean_df['Release_Date'] = pd.to_datetime(raw_df['Release_Date'], format='%m/%d/%Y')
# clean_df['Release_Date'] = raw_df['Release_Date'].apply(convert_str_to_date)

# convert USD_Worldwide_Gross --> float
clean_df['USD_Production_Budget'] = raw_df["USD_Production_Budget"].apply(lambda i: i.replace("$", ""))
clean_df['USD_Production_Budget'] = raw_df["USD_Production_Budget"].apply(lambda i: i.replace(",", ""))
clean_df['USD_Production_Budget'] = pd.to_numeric(clean_df['USD_Production_Budget'] )

clean_df['USD_Domestic_Gross'] = raw_df["USD_Domestic_Gross"].apply(lambda i: i.replace("$", ""))
clean_df['USD_Domestic_Gross'] = raw_df["USD_Domestic_Gross"].apply(lambda i: i.replace(",", ""))
clean_df['USD_Domestic_Gross'] = pd.to_numeric(clean_df['USD_Domestic_Gross'] )

clean_df['USD_Worldwide_Gross'] = raw_df["USD_Worldwide_Gross"].apply(lambda i: i.replace("$", ""))
clean_df['USD_Worldwide_Gross'] = raw_df["USD_Worldwide_Gross"].apply(lambda i: i.replace(",", ""))
clean_df['USD_Worldwide_Gross'] = pd.to_numeric(clean_df['USD_Worldwide_Gross'] )
print(clean_df)

# Get the nulls -- Count and records
print("=="*50)
t = clean_df.isna()
# print("Count of nulls on columns is:", t.sum())
print("Count of nulls is:", t.values.sum())
# print(raw_df[t.values])  # apply mask in dataframe

# Get the duplicates -- Count and records
t = raw_df.duplicated().values.sum()
# t = clean_df['Movie_Title'].duplicated().values.sum()
# # print(clean_df[clean_df['Movie_Title'].duplicated()].sort_values("Movie_Title"))
print("Count of duplicates is:", t)
# clean_df.drop_duplicates(("Movie_Title"), inplace=True)
# # print(clean_df[clean_df['Movie_Title'] == "Around the World in 80 Days"])
# t = clean_df['Movie_Title'].duplicated().values.sum()
# print("Count of duplicates post cleanse is:", t)

"""Challenge 1
What is the average production budget of the films in the data set?

What is the average worldwide gross revenue of films?

What were the minimums for worldwide and domestic revenue?

Are the bottom 25% of films actually profitable or do they lose money?

What are the highest production budget and highest worldwide gross revenue of any film?

How much revenue did the lowest and highest budget films make?

"""
t = round(clean_df['USD_Production_Budget'].mean())
print("Average production budget of the films: ", t)
t = round(clean_df['USD_Worldwide_Gross'].mean())
print("Average worldwide gross revenue of films: ", t)
t1 = round(clean_df['USD_Worldwide_Gross'].min())
t2 = round(clean_df['USD_Domestic_Gross'].min())
print("Minimums for worldwide and domestic revenue: ", t1, t2)
clean_df['Net_Revenue'] = (clean_df['USD_Domestic_Gross'] + clean_df['USD_Worldwide_Gross']) - \
                           clean_df['USD_Production_Budget']
t = clean_df["Net_Revenue"].sort_values()
bottom_25 = t[:round(len(t)/4)]
res = bottom_25 > 0
print("The count of profitable films in bottom 25%: ", res.sum())



# What are the highest production budget and highest worldwide gross revenue of any film?
t1 = clean_df["USD_Production_Budget"].max()
t2 = clean_df["USD_Domestic_Gross"] + clean_df["USD_Worldwide_Gross"]
t2 = round(t2.max())
print("Highest production budget and highest worldwide gross revenue of any film: ", t1, t2)

# How much revenue did the lowest and highest budget films make?
t = clean_df.sort_values("Net_Revenue")
lowest = t["Net_Revenue"][0]
highest = t["Net_Revenue"][len(t["Net_Revenue"]) - 1]
print("Revenue the lowest and highest budget films made: ", lowest, highest)


"""
Challenge 2
How many films grossed $0 domestically (i.e., in the United States)? What were the highest budget films that grossed nothing?
"""

# remove USD $0's
# # t = clean_df[(clean_df['USD_Worldwide_Gross'] == 0 | clean_df['USD_Worldwide_Gross'] == 0 )]
non_zero_revenue_df = clean_df['USD_Domestic_Gross'] == 0
print("How many films grossed $0 domestically: ", non_zero_revenue_df.values.sum())
# # print(clean_df[non_zero_revenue_df])
# clean_df.drop(clean_df[non_zero_revenue_df].index, inplace=True)
# print(non_zero_revenue_df.info)

non_zero_revenue_df = clean_df[non_zero_revenue_df]
non_zero_revenue_df.sort_values("USD_Production_Budget", ascending=False, inplace=True)
print("What were the highest budget films that grossed nothing?")
print(non_zero_revenue_df[["Release_Date", "Movie_Title", "USD_Production_Budget", "USD_Worldwide_Gross"]].head())


"""
Challenge 3
How many films grossed $0 worldwide? What are the highest budget films that had no revenue internationally (i.e., 
the biggest flops)?
"""
non_zero_revenue_df = clean_df['USD_Worldwide_Gross'] == 0
print("How many films grossed $0 worldwide: ", non_zero_revenue_df.values.sum())

non_zero_revenue_df = clean_df[non_zero_revenue_df]
non_zero_revenue_df.sort_values("USD_Production_Budget", ascending=False, inplace=True)
print("What are the highest budget films that had no revenue internationally?")
print(non_zero_revenue_df[["Release_Date", "Movie_Title", "USD_Production_Budget", "USD_Worldwide_Gross"]].head())


"""
which films made money internationally (i.e., data.USD_Worldwide_Gross != 0), but had zero box office revenue \
in the United States (i.e., data.USD_Domestic_Gross == 0)? 
"""
r = clean_df.loc[(clean_df["USD_Worldwide_Gross"]!= 0) & (clean_df["USD_Domestic_Gross"]== 0) ]
# print(r)


"""
Challenge
Use the Pandas .query() function to accomplish the same thing. Create a subset for international releases that 
had some worldwide gross revenue, but made zero revenue in the United States.

Hint: This time you'll have to use the and keyword.
"""
rr = clean_df.query('USD_Worldwide_Gross!= 0 and USD_Domestic_Gross== 0')
# print(rr)

"""
Challenge
Identify which films were not released yet as of the time of data collection (May 1st, 2018).

How many films are included in the dataset that have not yet had a chance to be screened in the box office? 

Create another DataFrame called data_clean that does not include these films.
"""
r1 = clean_df.loc[clean_df["Release_Date"] > datetime.datetime.strptime("01/May/2018", "%d/%b/%Y")]
clean_df.drop(r1.index, inplace=True)
print(clean_df.shape)


"""
Having removed the unreleased films entirely can you calculate the percentage of films that did not break even
at the box office? We already saw that more than the bottom quartile of movies appears to lose money when we
ran .describe(). However, what is the true percentage of films where the costs exceed the worldwide gross revenue?
"""
r3 = clean_df[clean_df["Net_Revenue"] < 0]
print("What is the true percentage of films where the costs exceed the worldwide gross revenue? ", len(r3))
# print(round((len(r3)/len(clean_df))*100, 2))

r3 = clean_df.query('USD_Production_Budget > (USD_Worldwide_Gross)')
print(round((len(r3)/len(clean_df))*100, 2))


import seaborn as sns
import matplotlib.pyplot as plt

def production_budget_vs_gross_worldwide_revenue_plot():
    # plt.figure(figsize=(8, 4), dpi=200)
    # set styling on a single chart
    with sns.axes_style('darkgrid'):
        ax = sns.scatterplot(data=clean_df,
                             x='USD_Production_Budget',
                             y='USD_Worldwide_Gross',
                             hue = 'USD_Worldwide_Gross',  # colour
                             size = 'USD_Worldwide_Gross')  # dot size

        ax.set(ylim=(0, 3000000000),
               xlim=(0, 450000000),
               ylabel='Revenue in $ billions',
               xlabel='Budget in $100 millions')

    plt.show()

def production_budget_vs_release_date_revenue_plot():
    ax = sns.scatterplot(data=clean_df, x="Release_Date", y="USD_Production_Budget", hue='USD_Worldwide_Gross',
                         size="USD_Worldwide_Gross")

    ax.set(ylim=(0, 450000000),
           xlim=(clean_df.Release_Date.min(), clean_df.Release_Date.max()),
           ylabel='Budget in $100 millions',
           xlabel='Release date')

    plt.show()


"""
Can you create a column in data_clean that has the decade of the movie release. For example, a film released in
1992 or 1999 should have 1990 in the Decade column.
"""
d_df = pd.DatetimeIndex(clean_df['Release_Date'])
# print((d_df.year//10)*10)
clean_df["Release_Decade"] = (d_df.year//10)*10
print(clean_df.head())


"""
Challenge
Create two new DataFrames: old_films and new_films

old_films should include all the films before 1970 (up to and including 1969)

new_films should include all the films from 1970 onwards

How many of our films were released prior to 1970?

What was the most expensive film made prior to 1970?
"""
old_films, new_films = clean_df[clean_df["Release_Decade"] < 1970], clean_df[clean_df["Release_Decade"] >= 1970]
print("How many of our films were released prior to 1970? ", len(old_films))
print("What was the most expensive film made prior to 1970? ", old_films["USD_Production_Budget"].max())


"""
This creates a scatter plot and draws a linear regression line together with the confidence interval at the same time.
"""
# sns.regplot(data=old_films,
#             x='USD_Production_Budget',
#             y='USD_Worldwide_Gross')
# plt.figure(figsize=(8,4), dpi=200)
# with sns.axes_style("whitegrid"):
#   sns.regplot(data=old_films,
#             x='USD_Production_Budget',
#             y='USD_Worldwide_Gross',
#             scatter_kws = {'alpha': 0.4},
#             line_kws = {'color': 'black'})
# plt.show()

"""
Use Seaborn's .regplot() to show the scatter plot and linear regression line against the new_films.

Style the chart

Put the chart on a 'darkgrid'.

Set limits on the axes so that they don't show negative values.

Label the axes on the plot "Revenue in $ billions" and "Budget in $ millions".

Provide HEX colour codes for the plot and the regression line. Make the dots dark blue (#2f4b7c) and the line orange (#ff7c43).
"""

# with sns.axes_style("darkgrid"):
#     ax = sns.regplot(data=new_films, x="USD_Production_Budget", y="USD_Worldwide_Gross",
#                 scatter_kws={'alpha': 0.4, 'color': '#2f4b7c'},
#                 line_kws={'color': '#ff7c43'})
#
#     ax.set(ylim=(new_films["USD_Worldwide_Gross"].min(), new_films["USD_Worldwide_Gross"].max()),
#            xlim=(new_films["USD_Production_Budget"].min(), new_films["USD_Production_Budget"].max()),
#            ylabel='Revenue in $ billions',
#            xlabel='Budget in $ millions')
#
# plt.show


from sklearn.linear_model import LinearRegression

regression = LinearRegression()

# Explanatory Variable(s) or Feature(s)
x = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
# Response Variable or Target
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

print(x.head())
# Find the best-fit line
regression.fit(x, y)

print(regression.coef_, regression.intercept_)
# R-squared
r_score = regression.score(x, y)
print("The r score of new films model is: ", r_score)

"""
You've just estimated the intercept and slope for the Linear Regression model. Now we can use it to make a prediction! For example, how much global revenue does our model estimate for a film with a budget of $350 million?
"""
def predict_revenue_based_on_budget(budget):
    y = regression.coef_*(budget) + regression.intercept_
    return y[0][0]

budget_inp = 350000000
res = predict_revenue_based_on_budget(budget_inp)
print(f"The estimated revenue on a movie with {budget_inp} budget is: {res}")