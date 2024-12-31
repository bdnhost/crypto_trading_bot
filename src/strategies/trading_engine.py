import numpy as np


class TradingStrategyEngine:
    def __init__(self, config):
        self.config = config

    def generate_trade_signal(self, prediction, risk_assessment):
        signal = "HOLD"
        if prediction > 0.7 and risk_assessment < 0.3:
            signal = "BUY"
        elif prediction < -0.7 and risk_assessment < 0.3:
            signal = "SELL"
        return TradeSignal(signal)


class TradeSignal:
    def __init__(self, action):
        self.action = action

    def is_executable(self):
        return self.action in ["BUY", "SELL"]
