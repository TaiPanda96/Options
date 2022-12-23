# Options

This is a options implementation with Postgres and Python, where Python primarily serves to process the ETL pipeline for Options Contracts.

A native Python Options Pricing model calculates the price of european options with slight adjustments:
To account for stocks with larger stock price swings, we use La Place Distribution instead. Theory here: 

Black Scholes model is slightly adjusted. Historical returns and standard deviation of historical returns are computed from 5 years of stock price changes. 

