import pandas as pd
import numpy as np


def calculate_rsi(
        ohlc: pd.DataFrame,
        period: int = 14,
        round_rsi: bool = True
):

    delta = ohlc["close"].diff()

    up = delta.copy()
    up[up < 0] = 0
    up = pd.Series.ewm(up, alpha=1/period).mean()

    down = delta.copy()
    down[down > 0] = 0
    down *= -1
    down = pd.Series.ewm(down, alpha=1/period).mean()

    rsi = np.where(
        up == 0, 0, np.where(down == 0, 100, 100 - (100 / (1 + up / down)))
    )

    return np.round(rsi, 2) if round_rsi else rsi


def calculate_vwap(data):
    typical_price = (data['high'] + data['low'] + data['close']) / 3
    vwap = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()
    return vwap
