# data/fetch.py

import datetime
import yfinance as yf
import pandas as pd

def get_underlying(ticker: str = "SPY") -> float:
    """
    Fetch the latest 1-minute close price for the given ticker.
    Returns:
        float: Last available close price.
    """
    # Download last 2 days of 1-min bars; pick the very last close
    df: pd.DataFrame = yf.download(
        tickers=ticker,
        period="2d",
        interval="1m",
        progress=False,
    )
    if df.empty:
        raise ValueError(f"No minute data returned for {ticker}")
    return float(df["Close"].iloc[-1])


def get_chain(ticker: str = "SPY") -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch today’s (0-DTE) option chain for the ticker.
    If today's expiry isn’t listed, picks the nearest upcoming expiry.
    Returns:
        calls (DataFrame), puts (DataFrame)
    """
    tk = yf.Ticker(ticker)
    # Get list of expiration dates as strings "YYYY-MM-DD"
    expiries = tk.options
    today_str = datetime.date.today().isoformat()

    # Choose expiry: prefer today, else the first one
    expiry = today_str if today_str in expiries else expiries[0]

    # Pull the option chain for that expiry
    chain = tk.option_chain(expiry)
    calls: pd.DataFrame = chain.calls
    puts: pd.DataFrame = chain.puts

    # Ensure bid/ask and IV columns exist
    for df in (calls, puts):
        for col in ["bid", "ask", "impliedVolatility"]:
            if col not in df.columns:
                raise KeyError(f"Column '{col}' missing from {ticker} {expiry} chain")

    return calls, puts
