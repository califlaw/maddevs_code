import websocket
import json
import pandas as pd
from calculation import calculate_rsi


class BinanceConn(websocket.WebSocketApp):
    def __init__(self, url, rsi_window):
        super().__init__(
            url,
            on_message=lambda ws, message: self.handle_message(message),
            on_error=lambda ws, error: print(error),
            on_close=lambda ws, close_status, close_msg: print(
                "Connection closed", close_msg
            )

        )
        self.rsi_window = rsi_window
        self.df = pd.DataFrame(columns=['close', 'RSI'])

    def handle_message(self, message):
        data = json.loads(message)
        kline = data['k']
        if kline['x']:
            close = float(kline['o'])
            self.df.loc[len(self.df)] = {'close': close}

            rsi_values = calculate_rsi(
                ohlc=self.df,
                period=self.rsi_window
            )
            self.df["RSI"] = rsi_values
