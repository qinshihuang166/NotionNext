"""
技术指标计算模块
Technical Indicators Calculator Module

计算各种常用的技术分析指标，用于特征工程
Calculate various technical analysis indicators for feature engineering

作者: qinshihuang166
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple


class TechnicalIndicators:
    """
    技术指标计算类
    
    包含常用的技术分析指标:
    - RSI (相对强弱指标)
    - MACD (移动平均收敛散度)
    - Bollinger Bands (布林带)
    - EMA (指数移动平均)
    - SMA (简单移动平均)
    - ATR (平均真实范围)
    - OBV (能量潮)
    - Stochastic Oscillator (随机振荡器)
    """
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        计算相对强弱指标 (RSI)
        
        RSI是动量振荡器，衡量价格变化的速度和变化
        范围: 0-100
        - RSI > 70: 超买区域
        - RSI < 30: 超卖区域
        
        Args:
            data: 价格数据 (通常是收盘价)
            period: 周期，默认14
            
        Returns:
            RSI值的Series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    @staticmethod
    def calculate_macd(data: pd.Series, 
                      fast_period: int = 12, 
                      slow_period: int = 26, 
                      signal_period: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        计算MACD (移动平均收敛散度)
        
        MACD是趋势跟踪动量指标
        - MACD线: 快速EMA - 慢速EMA
        - 信号线: MACD的EMA
        - 柱状图: MACD - 信号线
        
        Args:
            data: 价格数据 (通常是收盘价)
            fast_period: 快速EMA周期，默认12
            slow_period: 慢速EMA周期，默认26
            signal_period: 信号线周期，默认9
            
        Returns:
            (MACD线, 信号线, 柱状图)
        """
        ema_fast = data.ewm(span=fast_period, adjust=False).mean()
        ema_slow = data.ewm(span=slow_period, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        
        return macd_line, signal_line, macd_histogram
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, 
                                 period: int = 20, 
                                 num_std: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        计算布林带 (Bollinger Bands)
        
        布林带显示价格的波动性和相对高低
        - 中轨: 移动平均线
        - 上轨: 中轨 + (标准差 × 倍数)
        - 下轨: 中轨 - (标准差 × 倍数)
        
        Args:
            data: 价格数据 (通常是收盘价)
            period: 周期，默认20
            num_std: 标准差倍数，默认2.0
            
        Returns:
            (上轨, 中轨, 下轨)
        """
        middle_band = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        """
        计算指数移动平均 (EMA)
        
        EMA对近期价格赋予更高权重
        
        Args:
            data: 价格数据
            period: 周期
            
        Returns:
            EMA值的Series
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_sma(data: pd.Series, period: int) -> pd.Series:
        """
        计算简单移动平均 (SMA)
        
        SMA是最基础的移动平均线
        
        Args:
            data: 价格数据
            period: 周期
            
        Returns:
            SMA值的Series
        """
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_atr(high: pd.Series, 
                     low: pd.Series, 
                     close: pd.Series, 
                     period: int = 14) -> pd.Series:
        """
        计算平均真实范围 (ATR)
        
        ATR衡量市场波动性
        - ATR高: 波动性大
        - ATR低: 波动性小
        
        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            period: 周期，默认14
            
        Returns:
            ATR值的Series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        计算能量潮 (OBV - On Balance Volume)
        
        OBV通过累计成交量来衡量买卖压力
        - 价格上涨 + 成交量: OBV增加
        - 价格下跌 + 成交量: OBV减少
        
        Args:
            close: 收盘价
            volume: 成交量
            
        Returns:
            OBV值的Series
        """
        obv = np.where(close > close.shift(), volume, 
                      np.where(close < close.shift(), -volume, 0))
        return pd.Series(obv, index=close.index).cumsum()
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, 
                            low: pd.Series, 
                            close: pd.Series, 
                            period: int = 14,
                            smooth_k: int = 3,
                            smooth_d: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        计算随机振荡器 (Stochastic Oscillator)
        
        随机振荡器比较收盘价与一定时期内的价格范围
        范围: 0-100
        - %K > 80: 超买
        - %K < 20: 超卖
        
        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            period: 周期，默认14
            smooth_k: %K平滑周期，默认3
            smooth_d: %D平滑周期，默认3
            
        Returns:
            (%K, %D)
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        k_smooth = k.rolling(window=smooth_k).mean()
        d = k_smooth.rolling(window=smooth_d).mean()
        
        return k_smooth, d
    
    @staticmethod
    def calculate_momentum(data: pd.Series, period: int = 10) -> pd.Series:
        """
        计算动量指标 (Momentum)
        
        动量衡量价格变化的速度
        
        Args:
            data: 价格数据
            period: 周期，默认10
            
        Returns:
            动量值的Series
        """
        return data.diff(period)
    
    @staticmethod
    def calculate_roc(data: pd.Series, period: int = 12) -> pd.Series:
        """
        计算变化率 (ROC - Rate of Change)
        
        ROC衡量价格的百分比变化
        
        Args:
            data: 价格数据
            period: 周期，默认12
            
        Returns:
            ROC值的Series
        """
        return ((data - data.shift(period)) / data.shift(period)) * 100
    
    @staticmethod
    def calculate_williams_r(high: pd.Series, 
                            low: pd.Series, 
                            close: pd.Series, 
                            period: int = 14) -> pd.Series:
        """
        计算威廉指标 (Williams %R)
        
        威廉指标衡量超买超卖情况
        范围: -100 到 0
        - %R > -20: 超买
        - %R < -80: 超卖
        
        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            period: 周期，默认14
            
        Returns:
            威廉指标值的Series
        """
        highest_high = high.rolling(window=period).max()
        lowest_low = low.rolling(window=period).min()
        
        williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
        
        return williams_r
    
    @classmethod
    def add_all_indicators(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        为数据框添加所有技术指标
        
        这是一个便捷方法，一次性添加所有常用指标
        
        Args:
            df: 包含OHLCV数据的DataFrame
               必需列: open, high, low, close, volume
               
        Returns:
            添加了技术指标的DataFrame
        """
        df = df.copy()
        
        print("📊 正在计算技术指标...")
        
        # 1. RSI
        df['RSI'] = cls.calculate_rsi(df['close'], period=14)
        print("  ✓ RSI")
        
        # 2. MACD
        macd, signal, hist = cls.calculate_macd(df['close'])
        df['MACD'] = macd
        df['MACD_signal'] = signal
        df['MACD_hist'] = hist
        print("  ✓ MACD")
        
        # 3. Bollinger Bands
        bb_upper, bb_middle, bb_lower = cls.calculate_bollinger_bands(df['close'])
        df['BB_upper'] = bb_upper
        df['BB_middle'] = bb_middle
        df['BB_lower'] = bb_lower
        df['BB_width'] = bb_upper - bb_lower  # 布林带宽度
        print("  ✓ Bollinger Bands")
        
        # 4. EMA
        df['EMA_12'] = cls.calculate_ema(df['close'], 12)
        df['EMA_26'] = cls.calculate_ema(df['close'], 26)
        df['EMA_50'] = cls.calculate_ema(df['close'], 50)
        print("  ✓ EMA")
        
        # 5. SMA
        df['SMA_20'] = cls.calculate_sma(df['close'], 20)
        df['SMA_50'] = cls.calculate_sma(df['close'], 50)
        print("  ✓ SMA")
        
        # 6. ATR
        df['ATR'] = cls.calculate_atr(df['high'], df['low'], df['close'])
        print("  ✓ ATR")
        
        # 7. OBV
        df['OBV'] = cls.calculate_obv(df['close'], df['volume'])
        print("  ✓ OBV")
        
        # 8. Stochastic
        stoch_k, stoch_d = cls.calculate_stochastic(df['high'], df['low'], df['close'])
        df['Stoch_K'] = stoch_k
        df['Stoch_D'] = stoch_d
        print("  ✓ Stochastic")
        
        # 9. Momentum
        df['Momentum'] = cls.calculate_momentum(df['close'])
        print("  ✓ Momentum")
        
        # 10. ROC
        df['ROC'] = cls.calculate_roc(df['close'])
        print("  ✓ ROC")
        
        # 11. Williams %R
        df['Williams_R'] = cls.calculate_williams_r(df['high'], df['low'], df['close'])
        print("  ✓ Williams %R")
        
        # 12. 额外的价格特征
        df['close_open_ratio'] = df['close'] / df['open']  # 收盘价/开盘价
        df['high_low_ratio'] = df['high'] / df['low']  # 最高价/最低价
        df['price_change'] = df['close'].pct_change()  # 价格变化率
        df['volume_change'] = df['volume'].pct_change()  # 成交量变化率
        print("  ✓ 额外价格特征")
        
        print(f"\n✅ 技术指标计算完成! 共添加 {len(df.columns) - 6} 个特征")
        
        return df


def test_indicators():
    """测试技术指标计算"""
    # 创建示例数据
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': 100 + np.random.randn(100).cumsum(),
        'high': 102 + np.random.randn(100).cumsum(),
        'low': 98 + np.random.randn(100).cumsum(),
        'close': 100 + np.random.randn(100).cumsum(),
        'volume': np.random.randint(1000, 10000, 100)
    })
    
    # 添加所有指标
    df_with_indicators = TechnicalIndicators.add_all_indicators(df)
    
    print("\n" + "="*60)
    print("数据框形状:", df_with_indicators.shape)
    print("\n前5行数据:")
    print(df_with_indicators.head())
    print("\n数据框信息:")
    print(df_with_indicators.info())
    print("="*60)
    
    return df_with_indicators


if __name__ == "__main__":
    print("技术指标计算模块测试\n")
    df = test_indicators()
    print("\n✅ 测试完成!")
