import pandas as pd
from binance.client import Client
import logging
import os
from dotenv import load_dotenv

# 加载环境变量
# Load environment variables
load_dotenv()

class BinanceUtility:
    """
    Binance API 助手类，用于获取市场数据
    Binance API helper class for fetching market data
    """
    def __init__(self, api_key=None, api_secret=None):
        # 如果没有提供API Key，可以尝试从环境变量获取，或者使用匿名访问（仅限公开接口）
        # If no API Key is provided, try getting from environment or use anonymous access (public endpoints only)
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        
        try:
            self.client = Client(self.api_key, self.api_secret)
            logging.info("Binance Client 成功初始化 / Binance Client initialized successfully")
        except Exception as e:
            logging.error(f"Binance Client 初始化失败: {e} / Failed to initialize Binance Client: {e}")
            self.client = None

    def fetch_historical_data(self, symbol, interval, start_str, end_str=None):
        """
        获取历史K线数据
        Fetch historical K-line data
        
        :param symbol: 交易对 (e.g., 'BTCUSDT')
        :param interval: 时间间隔 (e.g., Client.KLINE_INTERVAL_1HOUR)
        :param start_str: 开始时间 (e.g., "1 Jan, 2023")
        :param end_str: 结束时间 (可选)
        :return: DataFrame
        """
        if not self.client:
            raise Exception("Binance Client 未初始化 / Binance Client not initialized")

        try:
            logging.info(f"正在从 Binance 获取 {symbol} 的历史数据... / Fetching historical data for {symbol} from Binance...")
            klines = self.client.get_historical_klines(symbol, interval, start_str, end_str)
            
            # 转换为 DataFrame
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # 数据预处理
            # Data preprocessing
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            logging.error(f"获取历史数据失败: {e} / Failed to fetch historical data: {e}")
            return None

    def get_realtime_price(self, symbol):
        """
        获取实时价格
        Get real-time price
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logging.error(f"获取实时价格失败: {e} / Failed to fetch real-time price: {e}")
            return None
