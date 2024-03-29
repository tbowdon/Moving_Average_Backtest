#!/usr/bin/env python
# coding: utf-8

# In[23]:


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# In[24]:


def get_stock_data(symbol, start_date, end_date):
    # Use yfinance to fetch historical stock data
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def calculate_moving_averages(data, short_window, long_window):
    # Calculate short-term and long-term moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

def simulate_trading_strategy(data, initial_balance=10000):
    # Initialize balance and position
    balance = initial_balance
    position = 0

    # Create a new column 'Signal' to store buy/sell signals
    data['Signal'] = None

    for i in range(1, len(data)):
        if data['Short_MA'][i] > 0 and data['Long_MA'][i] > 0:
            # Buy signal
            if data['Short_MA'][i] > data['Long_MA'][i] and data['Short_MA'][i - 1] <= data['Long_MA'][i - 1]:
                data.at[data.index[i], 'Signal'] = 'BUY'
                position = balance / data['Close'][i]
                balance = 0

            # Sell signal
            elif data['Short_MA'][i] <= data['Long_MA'][i] and data['Short_MA'][i - 1] > data['Long_MA'][i - 1]:
                data.at[data.index[i], 'Signal'] = 'SELL'
                balance = position * data['Close'][i]
                position = 0

    # Handle the last day's position
    if position > 0:
        data.at[data.index[-1], 'Signal'] = 'SELL'
        balance = position * data['Close'][-1]
        position = 0

    # Calculate final portfolio balance
    final_balance = balance + position * data['Close'][-1]

    # Other performance metrics calculations can be added here

    return data, {'final_balance': final_balance}


# In[25]:


symbol = input("Enter stock symbol: ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")


# In[28]:


# Get stock data
stock_data = get_stock_data(symbol, start_date, end_date)

# Set short and long moving average windows
short_window = 15
long_window = 45

# Calculate moving averages
stock_data = calculate_moving_averages(stock_data, short_window, long_window)

# Simulate trading strategy
final_data, final_balance = simulate_trading_strategy(stock_data)


# In[27]:


print("Final Portfolio Balance: $", round(final_balance['final_balance'],2))
# Display other summary statistics

# Plot the stock prices and moving averages
plt.figure(figsize=(10, 6))
plt.plot(final_data['Close'], label='Stock Price')
plt.plot(final_data['Short_MA'], label=f'Short MA ({short_window} days)')
plt.plot(final_data['Long_MA'], label=f'Long MA ({long_window} days)')
plt.title(f'{symbol} Moving Average Trading Strategy')
plt.legend()
plt.show()


# In[29]:


final_data

