import websocket
import json
from calculation import calculate_vwap
import pandas as pd


class BitfinexConn(websocket.WebSocketApp):
    def __init__(self, url, rsi_window):
        super().__init__(
            url,
            on_message=lambda ws, message: self.handle_message(message),
            on_open=lambda ws: self.send(
                '{ "event": "subscribe",  '
                '"channel": "candles",  "key": '
                '"trade:1m:tBTCUSD" }'
            ),
            on_error=lambda ws, error: print(error),
            on_close=lambda ws, close_status, close_msg: print(
                "Connection closed", close_msg
            )

        )
        self.rsi_window = rsi_window
        self.df = pd.DataFrame(
            columns=[
                'close',
                'high',
                'low',
                'volume',
                'vwap'
            ]
        )

    def handle_message(self, message):
        data = json.loads(message)
        current_data = data[1]
        if current_data == "hb" and len(data) >= 2:
            pass
        else:
            candle_data = {
                'close': current_data[2],
                'high': current_data[3],
                'low': current_data[4],
                'volume': current_data[5]
            }
            self.df['close'] = candle_data['close']
            self.df['high'] = candle_data['high']
            self.df['low'] = candle_data['low']
            self.df['volume'] = candle_data['volume']

        if len(self.df) >= 2:
            vwap = calculate_vwap(self.df)
            self.df['vwap'] = vwap
