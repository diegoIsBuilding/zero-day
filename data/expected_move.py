# data/expected_move.py

import math
from typing import Union

def one_day_sigma(
    spot_price: float,
    iv_annual: float,
    trading_days: int = 252
) -> float:
    """
    Calculate the 1-day ±1σ expected move in dollar terms
    given an annualized implied volatility.

    Args:
        spot_price (float): Current underlying price (e.g., SPY at $450).
        iv_annual (float): Annualized implied volatility (as a decimal, e.g., 0.20 for 20%).
        trading_days (int): Number of trading days per year (default 252).

    Returns:
        float: Dollar amount representing one standard deviation move for one day.
    """
    # Convert annual IV to daily volatility factor
    daily_vol = iv_annual / math.sqrt(trading_days)
    # Dollar move = spot_price × daily_vol
    return spot_price * daily_vol


def expected_move_range(
    spot_price: float,
    iv_annual: float,
    trading_days: int = 252
) -> tuple[float, float]:
    """
    Return the lower and upper price boundaries representing ±1σ move.

    Args:
        spot_price (float): Current price.
        iv_annual (float): Annual vol as decimal.
        trading_days (int): Trading days per year.

    Returns:
        (low, high): Tuple of floats = (spot_price - move, spot_price + move).
    """
    move = one_day_sigma(spot_price, iv_annual, trading_days)
    return spot_price - move, spot_price + move
