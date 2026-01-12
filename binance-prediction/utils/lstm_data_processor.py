"""
LSTM 数据处理模块
LSTM Data Processing Module

专门为LSTM模型处理时间序列数据
Specifically processes time-series data for LSTM models

作者: qinshihuang166
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from typing import Tuple, Optional, List
import joblib
import os

# 导入配置
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_lstm import DataConfig, PathConfig
from utils.technical_indicators import TechnicalIndicators


class LSTMDataProcessor:
    """
    LSTM数据处理器
    
    主要功能:
    1. 数据清洗和预处理
    2. 特征工程（技术指标）
    3. 数据归一化
    4. 创建时间序列窗口（滑动窗口）
    5. 数据集划分（训练/验证/测试）
    """
    
    def __init__(self, config: Optional[DataConfig] = None):
        """
        初始化数据处理器
        
        Args:
            config: 数据配置对象，默认使用全局配置
        """
        self.config = config or DataConfig()
        self.scaler = None
        self.feature_columns = None
        
    def load_raw_data(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        加载原始数据
        
        Args:
            file_path: 数据文件路径，默认使用配置中的路径
            
        Returns:
            原始数据DataFrame
        """
        file_path = file_path or self.config.RAW_DATA_FILE
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"❌ 数据文件不存在: {file_path}\n"
                f"请先运行 download_data.py 下载数据！"
            )
        
        print(f"📂 加载数据: {file_path}")
        df = pd.read_csv(file_path)
        
        # 确保必需的列存在
        required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"❌ 数据缺少必需列: {missing_cols}")
        
        # 转换时间戳
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        
        print(f"✓ 数据加载完成: {df.shape[0]} 行, {df.shape[1]} 列")
        print(f"  时间范围: {df.index[0]} 到 {df.index[-1]}")
        
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据
        
        处理:
        1. 删除重复行
        2. 排序时间序列
        3. 处理缺失值
        4. 移除异常值（可选）
        
        Args:
            df: 原始数据
            
        Returns:
            清洗后的数据
        """
        df = df.copy()
        print("\n🧹 开始数据清洗...")
        
        # 1. 删除重复行
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"  ⚠️ 发现 {duplicates} 个重复行，正在删除...")
            df = df[~df.duplicated()]
        
        # 2. 排序（时间序列必须按时间排序）
        df = df.sort_index()
        
        # 3. 检查缺失值
        missing = df.isnull().sum()
        if missing.any():
            print(f"  ⚠️ 发现缺失值:")
            for col, count in missing[missing > 0].items():
                print(f"    - {col}: {count} 个")
            
            # 向前填充（时间序列常用方法）
            df = df.fillna(method='ffill').fillna(method='bfill')
            print(f"  ✓ 缺失值已填充")
        
        # 4. 移除价格为0或负数的异常行
        invalid_rows = (df['close'] <= 0) | (df['volume'] < 0)
        if invalid_rows.any():
            print(f"  ⚠️ 发现 {invalid_rows.sum()} 个异常行（价格≤0或成交量<0），正在删除...")
            df = df[~invalid_rows]
        
        print(f"✅ 数据清洗完成: {df.shape[0]} 行保留")
        
        return df
    
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加特征（技术指标）
        
        Args:
            df: 清洗后的数据
            
        Returns:
            添加特征后的数据
        """
        print("\n🔧 开始特征工程...")
        
        # 使用技术指标类添加所有指标
        df = TechnicalIndicators.add_all_indicators(df)
        
        # 删除包含NaN的行（技术指标计算初期会有NaN）
        initial_rows = df.shape[0]
        df = df.dropna()
        dropped_rows = initial_rows - df.shape[0]
        
        if dropped_rows > 0:
            print(f"  ℹ️ 删除了 {dropped_rows} 行（技术指标计算初期的NaN）")
        
        print(f"✅ 特征工程完成: 当前共 {df.shape[1]} 个特征")
        
        return df
    
    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        选择用于训练的特征
        
        Args:
            df: 包含所有特征的数据
            
        Returns:
            仅包含选定特征的数据
        """
        # 基础OHLCV特征
        base_features = ['open', 'high', 'low', 'close', 'volume']
        
        # 从配置中获取技术指标特征
        if self.config.USE_TECHNICAL_INDICATORS:
            # 使用配置中指定的指标
            selected_features = base_features + self.config.TECHNICAL_INDICATORS
        else:
            selected_features = base_features
        
        # 检查哪些特征实际存在
        available_features = [f for f in selected_features if f in df.columns]
        missing_features = [f for f in selected_features if f not in df.columns]
        
        if missing_features:
            print(f"  ⚠️ 以下特征不存在，将被跳过: {missing_features}")
        
        print(f"  ✓ 选择了 {len(available_features)} 个特征: {available_features}")
        
        self.feature_columns = available_features
        return df[available_features]
    
    def normalize_data(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        归一化数据
        
        Args:
            df: 要归一化的数据
            fit: 是否拟合scaler（训练集用True，测试集用False）
            
        Returns:
            归一化后的数据
        """
        if fit:
            print("\n📏 开始数据归一化...")
            
            # 创建scaler
            if self.config.SCALER_TYPE == 'MinMaxScaler':
                self.scaler = MinMaxScaler(feature_range=self.config.FEATURE_RANGE)
            elif self.config.SCALER_TYPE == 'StandardScaler':
                self.scaler = StandardScaler()
            else:
                raise ValueError(f"不支持的scaler类型: {self.config.SCALER_TYPE}")
            
            # 拟合并转换
            scaled_data = self.scaler.fit_transform(df)
            print(f"  ✓ 使用 {self.config.SCALER_TYPE} 归一化")
            print(f"  ✓ 数据范围: {self.config.FEATURE_RANGE if self.config.SCALER_TYPE == 'MinMaxScaler' else '标准化'}")
        else:
            if self.scaler is None:
                raise ValueError("❌ Scaler尚未拟合，请先在训练集上调用fit=True")
            
            # 仅转换
            scaled_data = self.scaler.transform(df)
        
        # 转换回DataFrame（保持列名）
        scaled_df = pd.DataFrame(scaled_data, columns=df.columns, index=df.index)
        
        return scaled_df
    
    def create_sequences(self, data: np.ndarray, 
                        time_steps: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        创建时间序列窗口（滑动窗口）
        
        LSTM需要3D输入: (样本数, 时间步长, 特征数)
        
        示例:
        如果time_steps=3, 数据=[1,2,3,4,5]
        则创建:
        X = [[1,2,3], [2,3,4]], y = [4, 5]
        
        Args:
            data: 归一化后的数据（2D numpy array）
            time_steps: 时间窗口大小，默认使用配置
            
        Returns:
            (X, y): X是3D数组，y是目标值
        """
        time_steps = time_steps or self.config.TIME_STEPS
        
        X, y = [], []
        
        for i in range(time_steps, len(data)):
            # X: 过去time_steps个时间点的所有特征
            X.append(data[i - time_steps:i])
            # y: 下一个时间点的收盘价（假设收盘价是第4列，索引3）
            # 注意：这里假设特征顺序为 [open, high, low, close, ...]
            y.append(data[i, 3])  # 索引3是close
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"  ✓ 创建序列: X shape = {X.shape}, y shape = {y.shape}")
        print(f"    - 样本数: {X.shape[0]}")
        print(f"    - 时间步长: {X.shape[1]}")
        print(f"    - 特征数: {X.shape[2]}")
        
        return X, y
    
    def split_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, ...]:
        """
        划分训练集、验证集、测试集
        
        注意：时间序列数据不能随机打乱，必须按时间顺序划分
        
        Args:
            X: 特征数据
            y: 目标数据
            
        Returns:
            (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        total_samples = len(X)
        
        # 计算分割点
        train_size = int(total_samples * self.config.TRAIN_RATIO)
        val_size = int(total_samples * self.config.VAL_RATIO)
        
        # 划分数据
        X_train = X[:train_size]
        y_train = y[:train_size]
        
        X_val = X[train_size:train_size + val_size]
        y_val = y[train_size:train_size + val_size]
        
        X_test = X[train_size + val_size:]
        y_test = y[train_size + val_size:]
        
        print(f"\n📊 数据集划分:")
        print(f"  训练集: {X_train.shape[0]} 样本 ({self.config.TRAIN_RATIO*100:.0f}%)")
        print(f"  验证集: {X_val.shape[0]} 样本 ({self.config.VAL_RATIO*100:.0f}%)")
        print(f"  测试集: {X_test.shape[0]} 样本 ({self.config.TEST_RATIO*100:.0f}%)")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def save_scaler(self, path: Optional[str] = None):
        """保存scaler以供预测时使用"""
        path = path or PathConfig.SCALER_PATH
        
        if self.scaler is None:
            raise ValueError("❌ Scaler尚未初始化")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.scaler, path)
        print(f"✓ Scaler已保存: {path}")
    
    def load_scaler(self, path: Optional[str] = None):
        """加载已保存的scaler"""
        path = path or PathConfig.SCALER_PATH
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Scaler文件不存在: {path}")
        
        self.scaler = joblib.load(path)
        print(f"✓ Scaler已加载: {path}")
    
    def process_all(self, file_path: Optional[str] = None, 
                   save_processed: bool = True) -> Tuple[np.ndarray, ...]:
        """
        完整的数据处理流程
        
        这是一个便捷方法，按顺序执行所有处理步骤
        
        Args:
            file_path: 原始数据文件路径
            save_processed: 是否保存处理后的数据
            
        Returns:
            (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        print("="*60)
        print("🚀 开始完整数据处理流程")
        print("="*60)
        
        # 1. 加载数据
        df = self.load_raw_data(file_path)
        
        # 2. 清洗数据
        df = self.clean_data(df)
        
        # 3. 添加特征
        df = self.add_features(df)
        
        # 4. 选择特征
        df = self.select_features(df)
        
        # 5. 归一化数据
        df_normalized = self.normalize_data(df, fit=True)
        
        # 6. 创建序列
        print("\n🔄 创建时间序列窗口...")
        X, y = self.create_sequences(df_normalized.values)
        
        # 7. 划分数据集
        X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(X, y)
        
        # 8. 保存scaler
        self.save_scaler()
        
        # 9. 保存处理后的数据（可选）
        if save_processed:
            self._save_processed_data(df_normalized)
        
        print("\n" + "="*60)
        print("✅ 数据处理流程完成!")
        print("="*60)
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def _save_processed_data(self, df: pd.DataFrame):
        """保存处理后的数据"""
        os.makedirs(self.config.LSTM_DATA_DIR, exist_ok=True)
        save_path = self.config.PROCESSED_DATA_FILE
        df.to_csv(save_path)
        print(f"✓ 处理后的数据已保存: {save_path}")


def test_processor():
    """测试数据处理器"""
    print("LSTM数据处理器测试\n")
    
    # 创建示例数据
    dates = pd.date_range('2023-01-01', periods=1000, freq='H')
    df = pd.DataFrame({
        'timestamp': dates,
        'open': 100 + np.random.randn(1000).cumsum(),
        'high': 102 + np.random.randn(1000).cumsum(),
        'low': 98 + np.random.randn(1000).cumsum(),
        'close': 100 + np.random.randn(1000).cumsum(),
        'volume': np.random.randint(1000, 10000, 1000)
    })
    
    # 保存示例数据
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/test_data.csv', index=False)
    
    # 创建处理器
    processor = LSTMDataProcessor()
    
    # 处理数据
    try:
        X_train, X_val, X_test, y_train, y_val, y_test = processor.process_all('data/test_data.csv')
        
        print(f"\n最终数据形状:")
        print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
        print(f"X_val: {X_val.shape}, y_val: {y_val.shape}")
        print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")
        
        print("\n✅ 测试成功!")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_processor()
