from binance.client import Client


class TradeExecutor:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def execute_trade(self, symbol, action, quantity):
        try:
            if action == "BUY":
                order = self.client.create_order(
                    symbol=symbol,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity,
                )
            elif action == "SELL":
                order = self.client.create_order(
                    symbol=symbol,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity,
                )
            return order
        except Exception as e:
            print(f"Trade execution error: {e}")
