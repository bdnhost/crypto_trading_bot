import yaml
from binance.client import Client
from src.data.aggregator import DataAggregator
from src.models.hybrid_ml import HybridMLModel
from src.strategies.trading_engine import TradingStrategyEngine
from src.execution.trade_executor import TradeExecutor


def load_config(path="config/settings.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()

    client = Client(config["binance"]["api_key"], config["binance"]["secret_key"])

    data_aggregator = DataAggregator(config)
    ml_model = HybridMLModel(config)
    strategy_engine = TradingStrategyEngine(config)
    trade_executor = TradeExecutor(client, config)

    # Main trading cycle
    market_data = data_aggregator.collect_data()
    processed_data = data_aggregator.preprocess_data(market_data)

    for symbol, data in processed_data.items():
        prediction = ml_model.predict(data[["open", "high", "low", "close", "volume"]])
        risk_assessment = np.mean(data["volatility"])

        trade_signal = strategy_engine.generate_trade_signal(
            prediction, risk_assessment
        )

        if trade_signal.is_executable():
            trade_executor.execute_trade(symbol, trade_signal.action, 0.001)


if __name__ == "__main__":
    main()
