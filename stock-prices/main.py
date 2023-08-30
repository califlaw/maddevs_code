from binance_stream import BinanceConn
from bitfinex_stream import BitfinexConn

binance_url = "wss://stream.binance.com:443/ws/btcusdt@kline_1s"
binance_conn = BinanceConn(url=binance_url, rsi_window=14)
binance_conn.run_forever()

bitfinex_url = 'wss://api-pub.bitfinex.com/ws/1'
bitfinex_conn = BitfinexConn(url=bitfinex_url, rsi_window=14)
bitfinex_conn.run_forever()
