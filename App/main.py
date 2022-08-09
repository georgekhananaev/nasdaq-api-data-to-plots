#!/usr/bin/python

import matplotlib.pyplot as plt
import requests
import pandas as pd
import pyautogui
import datetime as dt
from sklearn.linear_model import LinearRegression
import dataFile

######################
######  SYSTEM  ######
######################

# getting your screen resolution
screen_w, screen_h = pyautogui.size()  # haven't tested on multi monitor computers.


# if plots doesn't open correctly you can set your resolution manually below, just unmask.
# screen_w = 1024
# screen_h = 768

######################
###### API CALL ######
######################

# get api data and create dataframe
def get_api_data(url: str):
    try:
        r = requests.get(
            url + dataFile.ApiData.data_type + '?api_key=' + dataFile.ApiData.api_key)  # setting workable api-url structure
        dataset = r.json()['dataset']  # getting into dataset
        data = pd.DataFrame((dataset['data']), columns=dataset['column_names'])  # from json creating normal dataframe
        data['Date'] = pd.to_datetime(data['Date'],
                                      format='%Y-%m-%d')  # change date format so future plots will be displayed from left to right.
        return data
    # handling errors
    except Exception as e:  # handling errors
        raise Exception(f"There is some issue with the API connection {e}")


# calling the function above and getting the data from the api url
api_data = get_api_data('https://data.nasdaq.com/api/v3/datasets/FSE/BDT_X')

###############################
######  TEMPORARY MEMORY  #####
###############################
# first up
first_consecutive_up_date = []
first_consecutive_up_close = []
first_consecutive_up_days = []
# last up
last_consecutive_up_date = []
last_consecutive_up_close = []
last_consecutive_up_days = []

# first down
first_consecutive_down_date = []
first_consecutive_down_close = []
first_consecutive_down_days = []
# last down
last_consecutive_down_date = []
last_consecutive_down_close = []
last_consecutive_down_days = []


######################
#### CALCULATIONS ####
######################

## function that getting data between two dates
# def get_data_between_dates(start_date, end_date):
#     data = get_api_data(api_data)
#     data = monthly_average()[(monthly_average()['Date'] > start_date) & (monthly_average()['Date'] <= end_date)]
#     return data


def get_sma(week, month, ninety):
    api_data.set_index('Date', inplace=True)  # setting date index for the plot
    reliance = api_data['Close'].to_frame()  # using .to_frame() to convert pandas series into dataframe.

    # calculating simple moving average week, month, ninety
    reliance[f'SMA {week} Days'] = reliance['Close'].rolling(week).mean()  # calculating simple moving average value
    reliance[f'SMA {month} Days'] = reliance['Close'].rolling(month).mean()
    reliance[f'SMA {ninety} Days'] = reliance['Close'].rolling(ninety).mean()
    reliance.dropna(inplace=True)  # deleting empty values using builtin function, disable or remove if not needed.
    return reliance


# grouping monthly average
def monthly_average():
    data = api_data.groupby(pd.PeriodIndex(api_data['Date'], freq="M"))['Close'].mean().reset_index()
    return data


# this is tasks 4, 5 will find how many consecutive days up or down you have in a dataframe.
def find_consecutive_days(consecutive_days: int, type: str):
    green_day_or_not = api_data['Open'] < api_data['Close']
    # noinspection PyTypeChecker
    days_with_condition = pd.DataFrame(
        list(zip(api_data['Date'], api_data['Open'], api_data['Close'], list(green_day_or_not))),
        columns=['Date', 'Open', 'Close', 'GreenDays'])
    # this is my loop to find 5 green days in row
    total_rows = len(api_data['Date'].index)  # total rows in your root file.
    five_green_days_counter = 0
    how_many_true = 0

    # decides which values to place in the loop below based on variable in the function.
    def if_up_or_down():
        if type == 'up':
            value_1 = 'True'
            value_2 = 'False'
            return [value_1, value_2]
        elif type == 'down':
            value_1 = 'False'
            value_2 = 'True'
            return [value_1, value_2]

    # this loop building new lists with needed data for our plot.
    for i in range(total_rows):
        if how_many_true == consecutive_days:
            five_green_days_counter += 1
            if type == 'up':
                # usually I am not working in production this way. Instead, looping values from dictionary list or other dataframe.
                first_consecutive_up_date.append(str(days_with_condition.iloc[i - 1]['Date']))
                last_consecutive_up_date.append(str(days_with_condition.iloc[i - consecutive_days]['Date']))
                first_consecutive_up_close.append(float(days_with_condition.iloc[i - 1]['Close']))
                last_consecutive_up_close.append(float(days_with_condition.iloc[i - consecutive_days]['Close']))
                first_consecutive_up_days.append(str(days_with_condition.iloc[i - 1]['GreenDays']))
                last_consecutive_up_days.append(str(days_with_condition.iloc[i - consecutive_days]['GreenDays']))
            elif type == 'down':
                first_consecutive_down_date.append(str(days_with_condition.iloc[i - 1]['Date']))
                last_consecutive_down_date.append(str(days_with_condition.iloc[i - consecutive_days]['Date']))
                first_consecutive_down_close.append(float(days_with_condition.iloc[i - 1]['Close']))
                last_consecutive_down_close.append(float(days_with_condition.iloc[i - consecutive_days]['Close']))
                first_consecutive_down_days.append(str(days_with_condition.iloc[i - 1]['GreenDays']))
                last_consecutive_down_days.append(str(days_with_condition.iloc[i - consecutive_days]['GreenDays']))
            else:
                print('wrong value entered')

        if if_up_or_down()[0] in str(days_with_condition.iloc[i]['GreenDays']):
            how_many_true += 1
        elif if_up_or_down()[1] in str(days_with_condition.iloc[i]['GreenDays']):
            how_many_true = 0
        i += 1
    print(f'This database has {five_green_days_counter} total consecutive {type} groups of {consecutive_days} days.')

    return days_with_condition


# calculates regression line based on period average
def regression_line_data():
    week_list = []  # temporary list for new data frame week
    month_list = []  # temporary list for new data frame month

    # grouping week/month/quarter and calculation average for each period
    group_week = api_data.groupby(pd.PeriodIndex(api_data['Date'], freq="W"))['Close'].mean().reset_index()
    group_month = api_data.groupby(pd.PeriodIndex(api_data['Date'], freq="M"))['Close'].mean().reset_index()
    quarter = api_data.groupby(pd.PeriodIndex(api_data['Date'], freq="Q"))['Close'].mean().reset_index()

    # this looping the date and rebuilding it.
    for i in group_week['Date']:
        day = str(i).split("/")[1]
        week_list.append(dt.datetime.strptime(day, '%Y-%m-%d').date())

    # changing week format
    week = pd.DataFrame(list(zip(week_list, group_week['Close'])), columns=['Date', 'Close'])

    # this looping the date and rebuilding it.
    for i in group_month['Date']:
        day = str(i) + '-01'
        month_list.append(dt.datetime.strptime(day, '%Y-%m-%d').date())

    # changing month format
    month = pd.DataFrame(list(zip(month_list, group_month['Close'])), columns=['Date', 'Close'])

    # changing quarter format to date time, in a clean way without re-write the whole thing.
    quarter['Date'] = pd.PeriodIndex(quarter['Date'], freq='Q').to_timestamp()

    return week, month, quarter


########################
######## GRAPHS ########
########################

# simple moving average plot
def sma_plot():
    try:
        # plotting simple moving average 7, 30 and 90 days question 1 based on "closed" values.
        get_sma(7, 30, 90)[['Close', 'SMA 7 Days', 'SMA 30 Days', 'SMA 90 Days']].plot(label='SMA', figsize=(
            screen_w / dataFile.AppData.plot_dpi, screen_h / dataFile.AppData.plot_dpi))
        plt.legend(loc='upper right')  # location of labels
        plt.savefig(dataFile.AppData.save_location + 'SMA 7-30-90 Days.pdf')  # save this plot as pdf
        plt.show()

    except Exception as e:
        print(e)
        pass


# subplots monthly average based on close data average
def monthly_average_plot():
    try:
        dates = monthly_average()['Date'].astype(dtype=str)
        values = monthly_average()['Close']
        fig, axs = plt.subplots(figsize=(screen_w / dataFile.AppData.plot_dpi, screen_h / dataFile.AppData.plot_dpi),
                                dpi=dataFile.AppData.plot_dpi)
        axs.bar(dates, values, label='Months')
        title_text = 'Monthly Average'
        fig.suptitle(title_text, fontsize=30)  # title
        plt.legend(loc='upper right')  # location of labels
        plt.savefig(dataFile.AppData.save_location + title_text + '.pdf')  # save this plot as pdf
        plt.show()
    except Exception as e:
        print(e)
        pass


# consecutive days plot, enter value up and down can be changed based on your requirements to find other dates
def consecutive_days_plot(up_value, down_value):
    try:
        find_consecutive_days(up_value, 'up')  # building data for up values
        find_consecutive_days(down_value, 'down')  # building data for down values

        fig = plt.figure(figsize=(screen_w / dataFile.AppData.plot_dpi, screen_h / dataFile.AppData.plot_dpi),
                         dpi=dataFile.AppData.plot_dpi)  # plot size based on your screen resolution

        # main line
        date = api_data['Date']
        open_values = api_data['Open']
        close_values = api_data['Close']

        # up values
        first_date_up = first_consecutive_up_date
        last_date_up = last_consecutive_up_date
        first_up = [x + 0.5 for x in first_consecutive_up_close]
        last_up = [x + 0.5 for x in last_consecutive_up_close]

        # down values
        first_date_down = first_consecutive_down_date
        last_date_down = last_consecutive_down_date
        first_down = [x - 0.5 for x in first_consecutive_down_close]
        last_down = [x - 0.5 for x in last_consecutive_down_close]

        # display plot
        plt.errorbar(date, close_values, label='Close')  # closed line
        plt.errorbar(date, open_values, label='Open')  # open line
        plt.scatter(first_date_up, first_up, marker="^", color='green',
                    label='first consecutive day up')  # first up
        plt.scatter(last_date_up, last_up, marker="^", color='blue', label='last consecutive day up')  # last up
        plt.scatter(first_date_down, first_down, marker="v", color='red',
                    label='first consecutive day down')  # first down
        plt.scatter(last_date_down, last_down, marker="v", color='purple',
                    label='last consecutive day down')  # last down
        title_text = f'{up_value} Consecutive days up and {down_value} down'
        fig.suptitle(title_text, fontsize=30)  # title
        plt.legend(loc='upper right')  # location of labels
        plt.savefig(dataFile.AppData.save_location + title_text + '.pdf')  # save this plot as pdf
        plt.show()  # show plot (needed only if running from cmd/terminal)
    except Exception as e:
        print(e)
        pass


# this is regression plot
def regression_line_plot():
    try:
        # this one getting returns from other function
        new_fixed_data = regression_line_data()[0]
        new_fixed_data_month = regression_line_data()[1]
        new_fixed_data_quarter = regression_line_data()[2]

        # Week liner
        new_fixed_data['Date'] = pd.to_datetime(new_fixed_data['Date'])  # changing the date to datetime with pandas.
        new_fixed_data['Date'] = new_fixed_data['Date'].map(
            dt.datetime.toordinal)  # changing the date to to-ordinal type, so it can be displayed on a liner.
        X = new_fixed_data.iloc[:, 0].values.reshape(-1, 1)  # column of X
        Y = new_fixed_data.iloc[:, 1].values.reshape(-1, 1)  # column of Y
        week_linear_regressor = LinearRegression()
        week_linear_regressor.fit(X, Y)
        y_liner = week_linear_regressor.predict(X)

        # Month liner
        new_fixed_data_month['Date'] = pd.to_datetime(
            new_fixed_data_month['Date'])  # changing the date to datetime with pandas.
        new_fixed_data_month['Date'] = new_fixed_data_month['Date'].map(
            dt.datetime.toordinal)  # changing the date to to-ordinal type, so it can be displayed on a liner.
        X_month = new_fixed_data.iloc[:, 0].values.reshape(-1, 1)  # column of X
        Y_month = new_fixed_data.iloc[:, 1].values.reshape(-1, 1)  # column of Y
        month_linear_regressor = LinearRegression()
        month_linear_regressor.fit(X_month, Y_month)
        month_liner = month_linear_regressor.predict(X)

        # Quarter liner
        new_fixed_data_quarter['Date'] = pd.to_datetime(
            new_fixed_data_quarter['Date'])  # changing the date to datetime with pandas.
        new_fixed_data_quarter['Date'] = new_fixed_data_quarter['Date'].map(
            dt.datetime.toordinal)  # changing the date to to-ordinal type, so it can be displayed on a liner.
        X_quarter = new_fixed_data.iloc[:, 0].values.reshape(-1, 1)  # column of X
        Y_quarter = new_fixed_data.iloc[:, 1].values.reshape(-1, 1)  # column of Y
        linear_regressor = LinearRegression()
        linear_regressor.fit(X_quarter, Y_quarter)
        quarter_liner = linear_regressor.predict(X)

        # 3 plots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(screen_w / dataFile.AppData.plot_dpi,
                                                           screen_h / dataFile.AppData.plot_dpi))  # change 3,1 to 1,3 if you want to change orientation
        title = 'Week, Month, Quarter regression lines'  # custom title, used multiple location
        fig.suptitle(title)  # fig title
        ax1.plot(X, Y)  # weekly plot
        ax1.plot(X, y_liner, color='red', label='Week')  # weekly plot liner
        ax2.plot(X_month, Y_month)  # monthly plot
        ax2.plot(X_month, month_liner, color='blue', label='Month')  # monthly plot liner
        ax3.plot(X_quarter, Y_quarter)  # quarter plot
        ax3.plot(X_quarter, quarter_liner, color='green', label='Quarter')  # quarter plot liner
        fig.legend(loc='upper right')  # location of labels
        plt.savefig(dataFile.AppData.save_location + title + '.pdf')  # save this plot as pdf
        plt.show()
    except Exception as e:
        print(e)
        pass


##########################
######### HELPERS ########
##########################
# # These helpers disabled by default, as I created menu.py file. However, enable them if you want to call functions manually.
# # data frames / other data outputs.
# print(api_data)  # print raw API data
# print(monthly_average())  # call for testing data
# find_consecutive_days(5, 'up')  # find consecutive days up or down

# #
# main.api_data.to_excel(f"{dataFile.AppData.save_location}output.xlsx", sheet_name='Sheet1') # save your API data to .xlsx file

# # plots
# sma_plot()  # call SMA plot for testing data
# monthly_average_plot()  # call for testing the plot
# consecutive_days_plot(5, 4)  # build a plot with consecutive days (up number, down number)
# regression_line_plot()
