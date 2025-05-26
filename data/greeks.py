# data/greeks.py

import math
from typing import Tuple

def norm_cdf(x: float) -> float:
    """
    Standard normal cumulative distribution function.
    """
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs_delta(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call: bool = True
) -> float:
    """
    Black–Scholes option delta.

    Args:
        S (float): Current underlying price.
        K (float): Option strike price.
        T (float): Time to expiry in years (e.g., 1/252 for one trading day).
        r (float): Risk-free interest rate (annual, decimal).
        sigma (float): Implied volatility (annual, decimal).
        call (bool): True for call delta, False for put delta.

    Returns:
        float: Option delta (between 0–1 for calls, -1–0 for puts).
    """
    if T <= 0 or sigma <= 0:
        # At expiry or zero volatility, delta is a step function
        intrinsic = 1.0 if (call and S > K) or (not call and S < K) else 0.0
        return intrinsic if call else intrinsic - 1.0

    d1 = (
        math.log(S / K)
        + (r + 0.5 * sigma ** 2) * T
    ) / (sigma * math.sqrt(T))
    delta = norm_cdf(d1) if call else norm_cdf(d1) - 1.0
    return delta

def bs_theta(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    call: bool = True
) -> float:
    """
    Black–Scholes option theta (time decay per year).

    Returns:
        float: Theta (negative means decay).
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    pdf = math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi)

    # Common factors
    term1 = - (S * pdf * sigma) / (2 * math.sqrt(T))
    term2 = r * K * math.exp(-r * T) * (norm_cdf(d2) if call else norm_cdf(-d2))

    return term1 - term2 if call else term1 + term2
