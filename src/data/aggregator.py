import pandas as pd
from binance.client import Client
import numpy as np

class DataAggregator:
    def __init__(self, config):
        self.client = Client(
            config['binance']['api_key'], 
            config['binance']['secret_key']
        )
        self.symbols = config['trading']['symbols']

    def collect_data(self, interval='1h', limit=100):
        all_data = {}
        for symbol in self.symbols:
            klines = self.client.get_klines(
                symbol=symbol, 
                interval=interval, 
                limit=limit
            )
            df = pd.DataFrame(klines, columns=[
                'open_time', 'open', 'high', 'low', 'close', 
                'volume', 'close_time', 'quote_av', 'trades', 
                'tb_base_av', 'tb_quote_av', 'ignore'
            ])
            df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
            all_data[symbol] = df
        return all_data

    def preprocess_data(self, market_data):
        processed_data = {}
        for symbol, df in market_data.items():
            df['returns'] = df['close'].pct_change()
            df['volatility'] = df['returns'].rolling(window=14).std()
            processed_data[symbol] = df
        return processed_data