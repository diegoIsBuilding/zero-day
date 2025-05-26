# logic/selector.py

from dataclasses import dataclass
from typing import Literal, Optional
from data.fetch import get_underlying, get_chain
from data.expected_move import one_day_sigma
from data.greeks import bs_delta

@dataclass
class Candidate:
    """
    A potential 0-DTE credit spread to place.
    """
    side: Literal["put", "call"]
    short_strike: float
    long_strike: float
    credit: float
    width: float
    delta: float

def pick_credit_spread(
    side: Literal["put", "call"],
    ticker: str = "SPY",
    min_credit: float = 0.15,
    max_width: float = 1.0,
    max_delta: float = 0.20,
    trading_days: int = 252
) -> Optional[Candidate]:
    """
    Scan today’s chain and pick the first credit spread 
    beyond ±1σ with acceptable width, credit, and delta.

    Returns:
        Candidate if found, else None.
    """
    # 1. Fetch live data
    price = get_underlying(ticker)
    calls, puts = get_chain(ticker)
    chain = puts if side == "put" else calls

    # 2. Compute 1-day ±1σ move
    #    (dollar amount = price × (iv / sqrt(days)))
    iv30 = float(chain["impliedVolatility"].mean())
    move = one_day_sigma(price, iv30, trading_days)

    # 3. Scan strikes outward
    for row in chain.itertuples():
        strike = row.strike
        # Determine if strike lies beyond the ±1σ boundary
        if side == "put" and strike < price - move or \
           side == "call" and strike > price + move:
            # 4. Compute mid-market credit
            credit = (row.bid + row.ask) / 2
            # 5. Calculate width and enforce max_width
            width = abs(row.strike - (strike - max_width if side=="put" else strike + max_width))
            if width > max_width or credit < min_credit:
                continue
            # 6. Compute option delta for risk filter
            delta = abs(bs_delta(price, strike, 1/trading_days, 0.0, iv30,
                                 call=(side=="call")))
            if delta >= max_delta:
                continue
            # 7. Build the Candidate with proper long_strike direction
            long_strike = strike - width if side == "put" else strike + width
            return Candidate(side, strike, long_strike, credit, width, delta)

    return None
