import yfinance as yf
import pandas as pd
from curl_cffi import requests as cureq
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import warnings, time, random, os
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# HTML Retrieval Error Handler
class HTMLRetrievalError(Exception):
    pass

# To GET HTML from URL and parse using BeautifulSoup
def retrieve_html(url, headers):
    results = cureq.get(url, headers=headers)
    if results.status_code != 200:
        for i in range(5):  # 5 retries in case of blokcing from bots
            time.sleep(5)
            results = cureq.get(url, headers=headers)
            if results.status_code == 200:
                break
    if results.status_code == 200:
        return BeautifulSoup(results.text, "html.parser")
    else:
        raise HTMLRetrievalError("Unable to parse blocked HTML contents!")

# Create graphs based on the stock data and revenue data
def make_graph(stock_data, revenue_data, stock):
    # Creating Subplots with two rows and one column]. shared_xaxes=True allows both plots to share the same x-axis (date) and vertical_spacing adjusts the space between the plots.
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3) 
    # Filtering Data to include only entries up to six months before the current dates. 
    # Get the current date
    current_date = datetime.now()
    # Subtract six months
    six_month_ago = current_date - relativedelta(months=6)
    # Format the date as YYYY-MM-DD
    formatted_date = six_month_ago.strftime('%Y-%m-%d')
    stock_data_specific = stock_data[stock_data.Date <= formatted_date]
    revenue_data_specific = revenue_data[revenue_data.Date <= formatted_date]
    # Adding Trace: Adds scatters plot for the stock prices and revenues. The x-axis is set to the dates (converted to datetime format). The name parameter specifies the legend label.
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    # Updating X-Axis and Y-Axis Titles
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    # Configures the overall layout of the figure.
    fig.update_layout(showlegend=False, # Hides the legend
    height=900,                         # Sets the height of the figure
    title=stock,                        # Assigns a title based on the stock name
    xaxis_rangeslider_visible=True)     # Enables a range slider for the x-axis, allowing users to zoom in on specific date ranges.
    fig.show()
    # Get the current script directory
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # Save the figure in the same folder as the Python script
    # pio.write_image(fig, os.path.join(script_dir, f"{stock}_stock_revenue.png"))
    
def main(symbol, stock):
    ticker = yf.Ticker(symbol)                   # Using the `Ticker` function enter the ticker symbol of the stock we want to extract
    ticker_data = ticker.history(period="max")    # Get information for the maximum amount of time
    ticker_data.reset_index(inplace=True)        # Reset dataFrame to the default integer index, and the old index will be added as a new column

    print(f"{stock} Data: (First 5 Rows)")
    print(ticker_data.head())

    # Webscrap Stock Revenue Data
    stock_url = f"https://www.macrotrends.net/stocks/charts/{symbol}/{stock.lower()}/revenue"
    # Create randomized user agents to simulate a real user
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    soup = retrieve_html(stock_url, headers=headers)
    stock_revenue = pd.DataFrame(columns=["Date", "Revenue"])

    for row in soup.find_all("tbody")[1].find_all('tr'):
        col = row.find_all("td")
        date = col[0].text
        revenue = col[1].text

        stock_revenue = pd.concat([stock_revenue,pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)  

    print(f"{stock} Revenue Data: (First 5 Rows)")
    print(stock_revenue.head())

    stock_revenue["Revenue"] = stock_revenue['Revenue'].str.replace(',',"").str.replace('$',"") # Remove the comma and dollar sign
    # Remove an null or empty strings in the Revenue column
    stock_revenue.dropna(inplace=True)
    stock_revenue = stock_revenue[stock_revenue['Revenue'] != ""]
    print(f"{stock} Revenue Data: (Last 5 Rows)")
    print(stock_revenue.tail())

    make_graph(ticker_data, stock_revenue, stock)

if __name__ == "__main__":
    # main("TSLA", "Tesla")
    # main("GME", "GameStop")
    main("AAPL", "Apple")