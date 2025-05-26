# logic/position.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

@dataclass
class Position:
    """
    Represents an open 0-DTE credit spread position with all
    relevant metadata for entry, risk management, and exit.
    """
    side: Literal["put", "call"]
    short_strike: float       # Strike of the option you sold
    long_strike: float        # Strike of the option you bought
    credit: float             # Net premium received (in dollars)
    width: float              # Distance between strikes (in dollars)
    delta: float              # Initial delta of the short leg
    entry_time: datetime      # Timestamp when the spread was opened

    # Risk limits (auto-computed)
    stop_credit: float = field(init=False)
    max_delta: float = 0.25   # Hard cap on delta for a forced exit

    def __post_init__(self):
        """
        After initialization, compute the absolute worst-case loss
        (stop_credit) as credit * stop_loss_multiplier (here 2× credit).
        """
        # If the spread moves against you by more than this,
        # you'll exit to cap the loss.
        self.stop_credit = self.credit * 2
