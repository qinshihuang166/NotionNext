import pandas as pd
import numpy as np

class DataProcessor:
    """
    数据处理类，用于特征工程和模型准备
    Data processing class for feature engineering and model preparation
    """
    
    @staticmethod
    def add_technical_indicators(df):
        """
        添加技术指标特征
        Add technical indicators as features
        """
        df = df.copy()
        
        # 移动平均线 (SMA)
        df['sma_7'] = df['close'].rolling(window=7).mean()
        df['sma_25'] = df['close'].rolling(window=25).mean()
        
        # 相对强弱指数 (RSI)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi_14'] = 100 - (100 / (1 + rs))
        
        # 价格变动率 (ROC)
        df['roc'] = df['close'].pct_change(periods=5)
        
        # 波动率 (Volatility)
        df['volatility'] = df['close'].rolling(window=7).std()
        
        # 移除缺失值
        df.dropna(inplace=True)
        return df

    @staticmethod
    def prepare_features_labels(df, target_col='close', horizon=1):
        """
        准备特征和标签：预测下一时期的价格变动
        Prepare features and labels: predict price movement of next period
        
        :param horizon: 预测的时步 (1 代表预测下个周期的涨跌)
        :return: X (features), y (labels)
        """
        # 目标：如果下个周期的收盘价高于当前收盘价，则为 1 (涨)，否则为 0 (跌)
        # Target: 1 if next period's close is higher than current, else 0
        df['target'] = (df[target_col].shift(-horizon) > df[target_col]).astype(int)
        
        # 特征列
        feature_cols = ['open', 'high', 'low', 'close', 'volume', 'sma_7', 'sma_25', 'rsi_14', 'roc', 'volatility']
        
        # 准备数据
        X = df[feature_cols][:-horizon]
        y = df['target'][:-horizon]
        
        return X, y
