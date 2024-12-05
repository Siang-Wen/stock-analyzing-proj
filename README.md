# stock-analyzing-proj
This is a Data Science Python project that extracts stock data and visualizes it through graph plots.

The Final Assignment is a Jupyter Notebook containing a comprehensive explanation of how to use the yfinance library to extract stock data and the plotly library to create a dashboard featuring graphs for the stock's daily closing price and revenue.

This shows how the yfinance library is implemented to retrieve stock data in DataFrame:
![Screenshot_yfinance_Ticker](https://github.com/user-attachments/assets/31e7eb6e-f3ff-4088-add0-502290374d28)

This shows how the dashboard created using the plotly library looks like:
![Screenshot_make_graph](https://github.com/user-attachments/assets/3afe50cb-9b6a-43a7-8410-472f28668473)

An additional Python script has been created to web scrape real-time stock revenue data, which includes a bot-blocking feature for the web scraping process. Furthermore, this Python script displays stock data for up to six months prior to the current date, rather than a specific date as shown in the Jupyter Notebook. To use the script, simply input the Ticker Symbol and Stock Name into the main() function, like this: main("AAPL", "Apple").
