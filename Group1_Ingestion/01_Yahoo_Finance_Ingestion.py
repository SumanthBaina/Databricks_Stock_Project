# Databricks notebook source
# COMMAND ----------
# Notebook: 01_Yahoo_Finance_Ingestion (LOCAL STORAGE VERSION)
# Description: Downloads stock data and saves it to Local Driver /tmp/ (Simulating Landing Zone)

%pip install yfinance

# COMMAND ----------
import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import shutil

# COMMAND ----------
# 1. Define Parameters
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
start_date = '2023-01-01' 
end_date = datetime.today().strftime('%Y-%m-%d')

# KEY CHANGE: Use Local Linux Filesystem ('/tmp/...') instead of DBFS
# This bypasses the "Public Root Disabled" error
local_landing_path = "/tmp/raw_stock_data/"

# Clean up previous run (Fresh start)
if os.path.exists(local_landing_path):
    shutil.rmtree(local_landing_path)

# Create Directory locally
os.makedirs(local_landing_path)

print(f"Local Landing Zone Ready: {local_landing_path}")

# COMMAND ----------
# 2. Download and Write (Standard Python I/O)
for ticker in tickers:
    print(f"Downloading {ticker}...")
    
    # Fetch Data
    pdf = yf.download(ticker, start=start_date, end=end_date)
    pdf = pdf.reset_index()
    
    # Convert Date to string
    pdf['Date'] = pdf['Date'].astype(str)
    pdf['Ticker'] = ticker
    
    # Construct filename
    filename = f"{ticker}_{datetime.now().strftime('%Y%m%d')}.json"
    full_path = f"{local_landing_path}{filename}"
    
    # Save as JSON to Local Disk
    pdf.to_json(full_path, orient='records', lines=False)
    print(f"Saved to: {full_path}")

print("-------------------------------------")
print("INGESTION COMPLETE.")
print(f"Files are located in: file:{local_landing_path}") 
# Note the 'file:' prefix - we will need this for Auto Loader later.