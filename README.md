# nasdaq-api-data-to-plots
Python script, which creates 4 different plot/graphs from Nasdaq API data.

![alt text](http://repository-images.githubusercontent.com/523085530/bf2d0c96-ae21-4fd8-a8e6-3e3887678f84)


#### What it doing:
1. retrieve data from https://data.nasdaq.com/api/v3/datasets/FSE/BDT_X (Frankfurt Stock Exchange). 
2. Display the 90,30,7 days moving average on a plot graph.
3. Display the monthly average price on that graph.
4. Detect and present (mark on the graph with a symbol, e.g. green triangle) the dates where there are 5 consecutive days of prices going up.
5. Detect and present the dates where there are 4 consecutive days of prices going down (different symbol).
6. Show on the graph a regression line.
7. Ability to save all data/plots from the API into files such as .xlsx, .pdfs formats.
8. Interactive Menu

## Get your own API KEY.
Register at: https://data.nasdaq.com/tools/api and place your key at: dataFile.py


## How to use in CMD/Terminal:

1. open cmd/terminal (colored package doesn't work in CMD, it will show some funny strings)
2. cd YOUR_PATCH/nasdaq-api-data-to-plots/App/
3. python3 menu.py or python menu.py

## How to open from your IDE:

Navigate: YOUR_PATCH/nasdaq-api-data-to-plots/App/
open main.py, go down and use helpers.

You can run each plot individually, by enabling/disabling with [HASH].

## Python Version:

Python 3.10.4 (Newer should work if available)

## If you installing libraries manually:

1.pip install requests
2.pip install matplotlib
3.pip install plotly
4.pip install pyautogui
5.pip install pandas
6.pip install datetime
7.pip install PyQt5
8.pip install scikit-learn
9.pip install termcolor
10.pip install colored (needed only for the menu.py)
11.sudo apt-get install python3-tk python3-dev

## All my Ubuntu libraries(can remove what you don't need):

located in: /nasdaq-api-data-to-plots/Documentation/
quick install: pip install -r YOUR_PATCH/nasdaq-api-data-to-plots/Documentation/requirements.txt

## Contact me:

Linkdin: linkedin.com/in/georgekhananaev

I won't approve anyone, you send me a message first. Thank you.
