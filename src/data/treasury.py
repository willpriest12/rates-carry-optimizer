# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 16:21:31 2025
Pulls an up-to-date treasury curve from FRED rates
@author: willp
"""
import pandas as pd
import requests
from io import StringIO
import pandas as pd
from curves.yield_curve import YieldCurve


FRED_SERIES = {
    "1M": "DGS1MO",
    "3M": "DGS3MO",
    "6M": "DGS6MO",
    "1Y": "DGS1",
    "2Y": "DGS2",
    "3Y": "DGS3",
    "5Y": "DGS5",
    "7Y": "DGS7",
    "10Y": "DGS10",
    "20Y": "DGS20",
    "30Y": "DGS30",
}

def fetch_treasury_curve():
    """
    Downloads daily Treasury yields for all maturities defined in FRED_SERIES.
    Returns a DataFrame:
        - Rows = calendar dates
        - Columns = maturities (1M, 2Y, 10Y, etc.)
        - Values = yields (percent per year)
    """
    cols = []   # this will hold one pandas Series per maturity (tenor)

    # Loop through each tenor (key) and its FRED ID (value)
    for tenor, sid in FRED_SERIES.items():
        # Construct the download URL for the CSV file on FRED
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

        # Download the CSV content as plain text from the web
        text = requests.get(url, timeout=30).text

        # Read the text into a pandas DataFrame as if it were a local CSV file
        df = pd.read_csv(StringIO(text))

        # Identify the first column (dates) and the second column (yield values).
        # We don’t assume the exact column names; we just take positions [0] and [1].
        date_col = df.columns[0]
        value_col = df.columns[1]

        # Convert the date column to pandas datetime objects
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

        # Set the date as the index and grab just the yield values
        s = df.set_index(date_col)[value_col]

        # Ensure the yield values are numeric (convert missing/invalid entries to NaN)
        s = pd.to_numeric(s, errors="coerce").rename(tenor)

        # Add this Series (for one maturity) to our list
        cols.append(s)

    # Combine all Series into one DataFrame (aligning by date).
    # Drop rows where *any* maturity is missing (ensures complete curves).
    out = pd.concat(cols, axis=1).dropna(how="any")

    # Return the final DataFrame: index = dates, columns = maturities, values = yields
    return out

def get_latest_curve():
    '''fetch most recent Treasury curve as a YieldCurve object'''
    df = fetch_treasury_curve()
    date = df.index[-1]
    row = df.iloc[-1]
    return YieldCurve(date, row)

def get_curve_on(date: str):
    '''fetch curve for a specific date (YYYY-MM-DD) as YieldCurve object'''
    df = fetch_treasury_curve()
    row = df.loc[date]
    return YieldCurve(pd.to_datetime(date), row)


    