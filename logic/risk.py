# logic/risk.py

from logic.position import Position
from typing import Optional

def should_exit(
    pos: Position,
    current_mid: float,
    current_delta: float,
    spot_price: float
) -> Optional[str]:
    """
    Decide whether to exit a credit spread position.

    Signals:
      - "target_hit":   mid ≤ 50% of credit  (profit target)
      - "stop_loss":    mid ≥ stop_credit OR delta ≥ max_delta
      - "breach":       spot_price beyond break-even
      - None:           hold position

    Args:
      pos:           Position object with entry metadata and risk limits
      current_mid:   current mid‐price of the spread (long price – short price)
      current_delta: current absolute delta of the short leg
      spot_price:    current underlying price

    Returns:
      A string signal or None to keep holding.
    """
    # 1) Profit target at 50% of received credit
    if current_mid <= pos.credit * 0.5:
        return "target_hit"

    # 2) Hard stop: max loss = pos.stop_credit OR delta breach
    if current_mid >= pos.stop_credit or current_delta >= pos.max_delta:
        return "stop_loss"

    # 3) Break-even breach: underlying crosses your break-even
    if pos.side == "put":
        breakeven = pos.short_strike + pos.credit
        if spot_price < breakeven:
            return "breach"
    else:  # call
        breakeven = pos.short_strike - pos.credit
        if spot_price > breakeven:
            return "breach"

    # 4) Otherwise, no exit signal
    return None
