import pandas as pd


pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.2f}'.format

df = pd.read_csv("salaries_by_college_major.csv")

print(df.info())
print(df.describe())

# Step-1: Look at the data

print("\nThe first 5 rows are:\n ", df.head())
print("\nThe columns are:\n", df.columns)
print("\nThe shape before cleaning is:\n", df.shape)


# Step-2: Clean the data
# Empty cell --> Clean nulls for all columns [Replace or drop]
# Wrong format --> Cast all columns to type
# Wrong data --> Set filters
# print(df['Mid-Career 90th Percentile Salary'].isna())
clean_df = df.dropna()
print("\nThe shape after cleaning - nulls is:\n", clean_df.shape)
# print(clean_df.info())

# find entry level with maximum salary --> Physician Assistant [
max_starter_salary = clean_df['Starting Median Salary'].max()
max_starter_salary_index = clean_df['Starting Median Salary'].idxmax()
print("\nHighest starting salary :", clean_df['Undergraduate Major'].loc[max_starter_salary_index], "and the salary is: "
      , max_starter_salary)


"""
What college major has the highest mid-career salary? How much do graduates with this major earn? 
(Mid-career is defined as having 10+ years of experience).

Which college major has the lowest starting salary and how much do graduates earn after university?

Which college major has the lowest mid-career salary and how much can people expect to earn with this degree? 
"""
highest_mid_career_salary_index = clean_df['Mid-Career Median Salary'].idxmax()
highest_mid_career_salary = clean_df['Mid-Career Median Salary'].max()
print("Max mid-career salary :", clean_df['Undergraduate Major'].loc[highest_mid_career_salary_index], "and the salary is: "
      , highest_mid_career_salary)



lowest_starting_salary_index = clean_df['Starting Median Salary'].idxmin()
lowest_starting_salary = clean_df['Starting Median Salary'].min()
print("Lowest starting salary :", clean_df['Undergraduate Major'].loc[lowest_starting_salary_index], "and the salary is: "
      , lowest_starting_salary)


lowest_mid_career_salary_index = clean_df['Mid-Career 10th Percentile Salary'].idxmin()
lowest_mid_career_salary = clean_df['Mid-Career 10th Percentile Salary'].min()
print("Min mid-career salary :", clean_df['Undergraduate Major'].loc[lowest_mid_career_salary_index], "and the salary is: "
      , lowest_mid_career_salary)


music_major_rows = clean_df.loc[clean_df['Undergraduate Major'] == 'Music']  # --> a mask is used to filter out records
average_salary_mid_career = music_major_rows['Mid-Career Median Salary'].mean()
print("Mean mid-career salary (Music):", average_salary_mid_career)


# get low risk major (Minimal spread)
spread_column_df = clean_df['Mid-Career 90th Percentile Salary'].subtract(clean_df['Mid-Career 10th Percentile Salary'])
clean_df.insert(1, "spread", spread_column_df)

# print("\nThe lowest spread field is:")
# min_spread = clean_df.loc[clean_df['spread'].idxmin()]
# print(min_spread)

print("\nThe 5 lowest spread field is:")
low_risk = clean_df.sort_values('spread')
print(low_risk[['Undergraduate Major', 'spread']].head())


"""
Using the .sort_values() method, can you find the degrees with the highest potential? Find the top 5 degrees with
the highest values in the 90th percentile. 

Also, find the degrees with the greatest spread in salaries. Which majors have the largest difference between high 
and low earners after graduation.
"""
print("\nThe 5 highest earning potential field is:")
top_5_potential_earners = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
print(top_5_potential_earners[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head())


print("\nThe 5 highest spread field is:")
high_risk = clean_df.sort_values('spread', ascending=False)
print(high_risk[['Undergraduate Major', 'spread']].head())



#
# URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"
# import requests
# from bs4 import BeautifulSoup
#
# response = requests.get(URL)
# response_html = response.text
#
# soup = BeautifulSoup(response_html, "html.parser")
# print(soup.prettify())
#
# data_list = []
# res = soup.find_all("tr", class_="data-table__row")
# for i in res:
#       k = i.find_all("span", class_="data-table__value")
#
#       rank = k[0].text
#       major = k[1].text
#       early_career_pay = k[3].text
#       mid_career_pay = k[4].text
#       data_list.append([rank, major, early_career_pay, mid_career_pay])
#
# for i in data_list:
#     print(i)
#
# with open("payscale_web_scraped_data", "w") as file:
#       for i in data_list:
#             acc = ""
#             for ii in i:
#                   acc += ii
#                   acc += "\t"
#             acc+= "\n"
#             file.write(acc)


row_holder_list = []
with open("payscale_web_scraped_data", "r") as file:
      for line in file:
            k = list(line.split("\t"))
            row_holder_list.append(k[:-1])

print(row_holder_list)

df = pandas.DataFrame(row_holder_list)
df.columns = ['Rank', 'Major', 'Early_career_pay', 'Mid_career_pay']
print(df.head())

print(df[['Major', 'Early_career_pay',]].sort_values('Early_career_pay', ascending=False).head())
print(df[['Major', 'Mid_career_pay']].sort_values('Mid_career_pay', ascending=False).head())
