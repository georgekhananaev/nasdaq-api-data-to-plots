# nasdaq-api-data-to-plots
Python script, which creates 4 different plot from Nasdaq API data.

#### What it doing:
1. retrieve data from https://data.nasdaq.com/api/v3/datasets/FSE/BDT_X (Frankfurt Stock Exchange). 
2. Display the 90,30,7 days moving average on a plot graph.
3. Display the monthly average price on that graph.
4. Detect and present (mark on the graph with a symbol, e.g. green triangle) the dates where there are 5 consecutive days of prices going up.
5. Detect and present the dates where there are 4 consecutive days of prices going down (different symbol).
6. Show on the graph a regression line.
7. Ability to save all data/plots from the API into files such as XLSX, pdfs.
8. Interactive Menu

## How to use in CMD/Terminal:

1. open cmd/terminal
2. cd YOUR_PATCH/nasdaq-api-data-to-plots/App/
3. python3 menu.py or python menu.py

## How to open from your IDE:

Navigate: YOUR_PATCH/nasdaq-api-data-to-plots/App/
open main.py, go down and use helpers.

You can run each plot individually, by enabling/disabling with [HASH].

## Python Version:

Python 3.10.4 (Newer should work if available)

## If you installing libraries manually:

pip install requests
pip install matplotlib
pip install plotly
pip install pyautogui
pip install pandas
pip install datetime
pip install PyQt5
pip install scikit-learn
pip install colored (needed only for the menu.py)

## All my Ubuntu libraries(can remove what you don't need):

located in: /nasdaq-api-data-to-plots/Documentation/
quick install: pip install -r YOUR_PATCH/nasdaq-api-data-to-plots/Documentation/requirements.txt

## Contact me:

Linkdin: linkedin.com/in/georgekhananaev

I won't approve anyone, you send me a message first. Thank you.
