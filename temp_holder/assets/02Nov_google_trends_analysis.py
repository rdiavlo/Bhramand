import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

tesla_df = pd.read_csv('data/google trends data/TESLA Search Trend vs Price.csv')
unemployment_excluding_covid_df = pd.read_csv('data/google trends data/UE Benefits Search vs UE Rate 2004-19.csv')
bitcoin_price_df = pd.read_csv('data/google trends data/Daily Bitcoin Price.csv')
bitcoin_popularity_df = pd.read_csv('data/google trends data/Bitcoin Search Trend.csv')
unemployment_including_covid_df = pd.read_csv('data/google trends data/UE Benefits Search vs UE Rate 2004-20.csv')

df_list = {"tesla_df": tesla_df, "unemployment_excluding_covid_df": unemployment_excluding_covid_df, "bitcoin_price_df": bitcoin_price_df,
           "bitcoin_popularity_df": bitcoin_popularity_df}

# for i in df_list:
#     print(df_list[i].head())
#     print(df_list[i].tail())
#     print("-"*68)


print("STEP-1 - CLEANING THE DATA: ")
def check_if_dataframe_has_nulls(df, df_name):
    num_of_rows = df.shape[0]
    print("The shape of dataframe", df.shape)
    columns = df.columns
    null_check = False
    print("The data frame has nulls:", df.isna().values.any())
    for col in columns:
        if df[col].notna().sum() < num_of_rows:
            count_of_nulls = num_of_rows - df[col].notna().sum()
            print(f"'{df_name}' data frame has {count_of_nulls} nulls in column {col}")

            null_check = True
    if not null_check:
        print(f"'{df_name}' data frame has no nulls")
        return False
    else:
        return True

print("==="*40)
for i in df_list:

    # print(i.info())
    if check_if_dataframe_has_nulls(df_list[i], i):
        # user_inp = input("Do you want to remove nulls? \n y/n")
        user_inp = "y"
        if user_inp == "y":
            df_list[i].dropna(inplace=True)
    print("-" * 68)


# Convert date field to date_time format
tesla_df['MONTH'] = pd.to_datetime(tesla_df['MONTH'])
unemployment_excluding_covid_df['MONTH'] = pd.to_datetime(unemployment_excluding_covid_df['MONTH'])
bitcoin_price_df['DATE'] = pd.to_datetime(bitcoin_price_df['DATE'])
bitcoin_popularity_df['MONTH'] = pd.to_datetime(bitcoin_popularity_df['MONTH'])
unemployment_including_covid_df['MONTH'] = pd.to_datetime(unemployment_including_covid_df['MONTH'])

bitcoin_price_MONTHLY_df = bitcoin_price_df.resample('M', on="DATE").last()
print(bitcoin_price_MONTHLY_df.head())
print("==="*40)

# Visually analyze the data


def plot_tesla():
    plt.figure(figsize=(14, 8), dpi=120)
    axis_1 = plt.gca()
    axis_2 = plt.twinx()

    axis_1.set_title("Tesla Web Search vs Price")
    axis_1.set_xlabel('Month', fontsize=14)
    axis_1.set_ylabel('Web searches', fontsize=14, color="green")
    axis_2.set_ylabel('Price', fontsize=14, color="orange")

    # Set the minimum and maximum values on the axes
    axis_1.set_ylim([0, tesla_df['TSLA_WEB_SEARCH'].max()])
    axis_1.set_xlim([tesla_df.MONTH.min(), tesla_df.MONTH.max()])
    axis_2.set_ylim([0, tesla_df['TSLA_USD_CLOSE'].max()])

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    # format the ticks
    axis_1.xaxis.set_major_locator(years)
    axis_1.xaxis.set_major_formatter(years_fmt)
    axis_1.xaxis.set_minor_locator(months)

    x, y = tesla_df['MONTH'], tesla_df['TSLA_WEB_SEARCH']
    axis_1.plot(x, y, color="green")

    x, y = tesla_df['MONTH'], tesla_df['TSLA_USD_CLOSE']
    axis_2.plot(x, y, color="orange")


def plot_bitcoin():
    # Bitcoin News Search vs Resampled Price
    plt.figure(figsize=(14, 8), dpi=120)
    axis_1 = plt.gca()
    axis_2 = plt.twinx()
    plt.title('Bitcoin News Search vs Resampled Price')
    axis_1.set_xlabel('Month', fontsize=14)
    axis_1.set_ylabel('Price', fontsize=14, color="orange")
    axis_2.set_ylabel('Popularity', fontsize=14, color="blue")

    # Set the minimum and maximum values on the axes
    axis_1.set_ylim([0, bitcoin_price_MONTHLY_df['CLOSE'].max()])
    axis_1.set_xlim([bitcoin_price_MONTHLY_df.index.min(), bitcoin_price_MONTHLY_df.index.max()])
    axis_2.set_ylim([0, bitcoin_popularity_df['BTC_NEWS_SEARCH'].max()])

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%d-%b-%Y')

    # format the ticks
    axis_1.xaxis.set_major_locator(years)
    axis_1.xaxis.set_major_formatter(years_fmt)
    axis_1.xaxis.set_minor_locator(months)

    x, y = bitcoin_price_MONTHLY_df.index, bitcoin_price_MONTHLY_df['CLOSE']
    axis_1.plot(x, y, color="orange", linestyle='dashed')

    color = "skyblue"
    x, y = bitcoin_popularity_df['MONTH'], bitcoin_popularity_df['BTC_NEWS_SEARCH']
    axis_2.plot(x, y, marker='o', color=color)


"""
Change the title to: Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate
Change the y-axis label to: FRED U/E Rate
Change the axis limits
Add a grey grid to the chart to better see the years and the U/E rate values. Use dashed lines for the line style.
Can you discern any seasonality in the searches? Is there a pattern?
"""

def plot_unrolled_pre_covid_unemployment(axis):
    # filter out covid --> check for seasonal patterns [This is mitigated by choosing pre-2020 dataset]
    # from datetime import datetime
    # unemployment_excluding_covid_df_pre_covid = unemployment_excluding_covid_df[unemployment_excluding_covid_df['MONTH'] < datetime.strptime('01/01/2020', "%d/%m/%Y")]

    unemployment_excluding_covid_df_pre_covid = unemployment_excluding_covid_df
    print(unemployment_excluding_covid_df_pre_covid.head())
    print(unemployment_excluding_covid_df_pre_covid['MONTH'].max())

    FONTSIZE = 10
    # axis.figure(figsize=(14, 8), dpi=120)
    axis.set_title("Monthly Search of 'Unemployment Benefits' in the U.S. vs the U/E Rate (Un-Rolled Mean)")
    axis.grid(color='black', linestyle='-', linewidth=0.2)
    # axis.yticks(fontsize=FONTSIZE)
    # axis.xticks(fontsize=FONTSIZE, rotation=45)

    axis_1 = axis
    axis_2 = axis_1.twinx()
    axis_1.set_xlabel('Month', fontsize=14)
    axis_1.set_ylabel('UE searches', fontsize=14, color="skyblue")
    axis_2.set_ylabel('UE rate', fontsize=14, color="purple")

    # set axis limits
    axis_1.set_ylim([unemployment_excluding_covid_df_pre_covid['UE_BENEFITS_WEB_SEARCH'].min(),
                     unemployment_excluding_covid_df_pre_covid['UE_BENEFITS_WEB_SEARCH'].max()])
    axis_2.set_ylim([unemployment_excluding_covid_df_pre_covid['UNRATE'].min(), unemployment_excluding_covid_df_pre_covid['UNRATE'].max()])
    axis_1.set_xlim([unemployment_excluding_covid_df_pre_covid['MONTH'].min(), unemployment_excluding_covid_df_pre_covid['MONTH'].max()])

    x, y = unemployment_excluding_covid_df_pre_covid['MONTH'], unemployment_excluding_covid_df_pre_covid['UE_BENEFITS_WEB_SEARCH']
    axis_1.plot(x, y, color="skyblue")
    x, y = unemployment_excluding_covid_df_pre_covid['MONTH'], unemployment_excluding_covid_df_pre_covid['UNRATE']
    axis_2.plot(x, y, color="purple", linestyle='dashed')



def plot_rolled_pre_covid_unemployment(axis):
    # filter out covid --> check for seasonal patterns [This is mitigated by choosing pre-2020 dataset]
    # from datetime import datetime
    # unemployment_excluding_covid_df_pre_covid = unemployment_excluding_covid_df[unemployment_excluding_covid_df['MONTH'] < datetime.strptime('01/01/2020', "%d/%m/%Y")]

    unemployment_excluding_covid_df_pre_covid = unemployment_excluding_covid_df
    print(unemployment_excluding_covid_df_pre_covid.head())

    roll_df = unemployment_excluding_covid_df_pre_covid[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()
    # print(roll_df.dropna(inplace=True))
    print(roll_df)

    print("checkkk")
    print(unemployment_excluding_covid_df_pre_covid['MONTH'].max())

    FONTSIZE = 10
    # plt.figure(figsize=(14, 8), dpi=120)
    axis.set_title("Monthly Search of 'Unemployment Benefits' in the U.S. vs the U/E Rate (Rolled Mean)")
    axis.grid(color='black', linestyle='-', linewidth=0.2)
    # plt.yticks(fontsize=FONTSIZE)
    # plt.xticks(fontsize=FONTSIZE, rotation=45)

    axis_1 = axis
    axis_2 = axis_1.twinx()
    axis_1.set_xlabel('Month', fontsize=14)
    axis_1.set_ylabel('UE searches', fontsize=14, color="skyblue")
    axis_2.set_ylabel('UE rate', fontsize=14, color="purple")

    # set axis limits
    # axis_1.set_ylim([unemployment_excluding_covid_df_pre_covid['UE_BENEFITS_WEB_SEARCH'].min(),
    #                     unemployment_excluding_covid_df_pre_covid['UE_BENEFITS_WEB_SEARCH'].max()])
    # axis_2.set_ylim([unemployment_excluding_covid_df_pre_covid['UNRATE'].min(), unemployment_excluding_covid_df_pre_covid['UNRATE'].max()])
    # axis_1.set_xlim([unemployment_excluding_covid_df_pre_covid['MONTH'].min(), unemployment_excluding_covid_df_pre_covid['MONTH'].max()])

    x, y = unemployment_excluding_covid_df_pre_covid['MONTH'], roll_df['UE_BENEFITS_WEB_SEARCH']
    axis_1.plot(x, y, color="skyblue")
    x, y = unemployment_excluding_covid_df_pre_covid['MONTH'], roll_df['UNRATE']
    axis_2.plot(x, y, color="purple", linestyle='dashed')




def plot_unrolled_including_covid_unemployment(axis):

    print(unemployment_including_covid_df.head())
    print(unemployment_including_covid_df['MONTH'].max())

    FONTSIZE = 6
    plt.figure(figsize=(14, 8), dpi=120)
    plt.title("Monthly Search of 'Unemployment Benefits' in the U.S. vs the U/E Rate [Inc Covid]")
    plt.grid(color='black', linestyle='-', linewidth=0.2)
    plt.yticks(fontsize=FONTSIZE)
    plt.xticks(fontsize=FONTSIZE, rotation=45)

    axis_1 = axis
    axis_2 = axis_1.twinx()
    axis_1.set_xlabel('Month', fontsize=14)
    axis_1.set_ylabel('UE searches', fontsize=14, color="skyblue")
    axis_2.set_ylabel('UE rate', fontsize=14, color="purple")

    # set axis limits
    axis_1.set_ylim([unemployment_including_covid_df['UE_BENEFITS_WEB_SEARCH'].min(),
                     unemployment_including_covid_df['UE_BENEFITS_WEB_SEARCH'].max()])
    axis_2.set_ylim([unemployment_including_covid_df['UNRATE'].min(), unemployment_including_covid_df['UNRATE'].max()])
    axis_1.set_xlim([unemployment_including_covid_df['MONTH'].min(), unemployment_including_covid_df['MONTH'].max()])

    x, y = unemployment_including_covid_df['MONTH'], unemployment_including_covid_df['UE_BENEFITS_WEB_SEARCH']
    axis_1.plot(x, y, color="skyblue")
    x, y = unemployment_including_covid_df['MONTH'], unemployment_including_covid_df['UNRATE']
    axis_2.plot(x, y, color="purple", linestyle='dashed')


fig, ax = plt.subplots(nrows=2, ncols=1)


plot_unrolled_pre_covid_unemployment(ax[0])
plot_rolled_pre_covid_unemployment(ax[1])
# plot_unrolled_including_covid_unemployment(ax[2])
plt.tight_layout()
plt.show()