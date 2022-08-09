#!/usr/bin/python

from termcolor import colored
import main
import time
from main import *


########################
########  MENU  ########
########################
def goodbye():
    print(colored('You pressed invalid or exit key, software will be closed...', 'blue'))
    time.sleep(1)
    print(colored('Thank you for using my little software.', 'yellow'))
    time.sleep(1)
    print(colored('Goodbye!', 'red'))


def plot_closed():
    print(colored('Unfortunately plot.show() breaking the loop.', 'red'))
    print(colored(f'Please re-open the menu again for another plot.', 'yellow'))
    for i in range(3, 0, -1):
        print(f'Will be closed in: {i}')
        time.sleep(1)


print(colored('Hi, do you want to export the api data to a file?', 'yellow'))
input_save_file = str(input('Type Yes/No (or press any key as no): '))
input_save_file = input_save_file.lower()
print(input_save_file)
if 'yes' == input_save_file:
    saved = colored('Your file saved to', 'blue')
    main.api_data.to_excel(f"{dataFile.AppData.save_location}output.xlsx", sheet_name='Sheet1')
    print(f'{saved} to {dataFile.AppData.save_location}')
else:
    print(colored('No file saved.', 'red'))

while True:
    print(colored('Select which plot you want to get:', 'yellow'))
    print('''
    Press:  
     [1]   To display 90,30,7 days simple moving average.
     [2]   To display Monthly average.
     [3]   To display 5 up, 4 down consecutive days.
     [4]   To display regression line for the last 90, 30 and 7 days.
    [Any]  To exit
    ''')

    select_plot = str(input('Type: 1,2,3,4 or press any key to EXIT: '))
    if '1' == select_plot:
        print(colored(f'Opening SMA Plot, a pdf file will be saved to: {dataFile.AppData.save_location}', 'yellow'))
        time.sleep(1)
        sma_plot()
        plot_closed()
        break

    elif '2' == select_plot:
        print(colored(f'Opening monthly average_plot, a pdf file will be saved to: {dataFile.AppData.save_location}',
                      'yellow'))
        time.sleep(1)
        monthly_average_plot()
        plot_closed()
        break

    elif '3' == select_plot:
        print(colored(f'Opening consecutive days plot, a pdf file will be saved to: {dataFile.AppData.save_location}',
                      'yellow'))
        time.sleep(1)
        consecutive_days_plot(5, 4)
        plot_closed()
        break

    elif '4' == select_plot:
        print(colored(f'Opening regression line plot, a pdf file will be saved to: {dataFile.AppData.save_location}',
                      'yellow'))
        time.sleep(1)
        regression_line_plot()
        plot_closed()
        break

    else:
        goodbye()
        break
