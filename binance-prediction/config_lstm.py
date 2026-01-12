"""
LSTM 模型配置文件
LSTM Model Configuration

这个文件包含所有可调整的超参数和配置选项
This file contains all tunable hyperparameters and configuration options

作者: qinshihuang166
日期: 2024
"""

import os
from typing import Dict, List, Tuple

# ============================================
# 数据配置 / Data Configuration
# ============================================

class DataConfig:
    """数据获取和处理配置"""
    
    # Binance API 配置
    SYMBOL = 'BTCUSDT'  # 交易对 / Trading pair
    INTERVAL = '1h'  # K线间隔: 1m, 5m, 15m, 1h, 4h, 1d / Candlestick interval
    LOOKBACK_DAYS = 365  # 获取多少天的历史数据 / Days of historical data
    
    # 数据路径配置
    DATA_DIR = 'data'  # 原始数据目录
    LSTM_DATA_DIR = 'lstm_data'  # LSTM处理后的数据目录
    RAW_DATA_FILE = f'{DATA_DIR}/{SYMBOL}_raw_data.csv'
    PROCESSED_DATA_FILE = f'{LSTM_DATA_DIR}/{SYMBOL}_processed.csv'
    
    # 数据划分比例
    TRAIN_RATIO = 0.70  # 70% 训练集
    VAL_RATIO = 0.15    # 15% 验证集
    TEST_RATIO = 0.15   # 15% 测试集
    
    # 特征工程配置
    USE_TECHNICAL_INDICATORS = True  # 是否使用技术指标
    TECHNICAL_INDICATORS = [
        'RSI',           # 相对强弱指标
        'MACD',          # 移动平均收敛散度
        'MACD_signal',   # MACD信号线
        'MACD_hist',     # MACD柱状图 (MACD - Signal)
        'BB_upper',      # 布林带上轨
        'BB_middle',     # 布林带中轨
        'BB_lower',      # 布林带下轨
        'EMA_12',        # 12期指数移动平均
        'EMA_26',        # 26期指数移动平均
        'ATR',           # 平均真实范围
        'OBV',           # 能量潮
    ]
    
    # 时间序列窗口配置
    TIME_STEPS = 60  # 使用过去60个时间点预测下一个 / Use past 60 timesteps to predict next one
    PREDICTION_HORIZON = 1  # 预测未来1个时间点 / Predict 1 timestep ahead
    
    # 数据归一化
    SCALER_TYPE = 'MinMaxScaler'  # 可选: 'MinMaxScaler', 'StandardScaler'
    FEATURE_RANGE = (0, 1)  # MinMaxScaler的范围


# ============================================
# 模型配置 / Model Configuration
# ============================================

class ModelConfig:
    """LSTM 模型架构配置"""
    
    # 模型类型
    MODEL_TYPE = 'BiLSTM'  # 可选: 'LSTM', 'BiLSTM', 'GRU', 'BiGRU'
    
    # 网络架构
    # 层配置格式: [第一层单元数, 第二层单元数, ...]
    LSTM_UNITS = [128, 64, 32]  # 三层LSTM，每层的单元数
    DENSE_UNITS = [16]  # Dense层配置
    
    # Dropout 配置（防止过拟合）
    DROPOUT_RATE = 0.2  # Dropout比例 (0.2 = 20%)
    RECURRENT_DROPOUT = 0.1  # LSTM内部的Dropout
    
    # 正则化配置（防止过拟合）
    USE_L1_REGULARIZATION = False  # 是否使用L1正则化
    USE_L2_REGULARIZATION = True   # 是否使用L2正则化
    L1_LAMBDA = 0.0001  # L1正则化系数
    L2_LAMBDA = 0.001   # L2正则化系数
    
    # BatchNormalization
    USE_BATCH_NORMALIZATION = True  # 是否使用批标准化
    
    # 激活函数
    LSTM_ACTIVATION = 'tanh'  # LSTM激活函数
    DENSE_ACTIVATION = 'relu'  # Dense层激活函数
    OUTPUT_ACTIVATION = 'linear'  # 输出层激活函数 (回归问题用linear)
    
    # 损失函数和优化器
    LOSS_FUNCTION = 'mse'  # 可选: 'mse', 'mae', 'huber'
    OPTIMIZER = 'adam'  # 可选: 'adam', 'rmsprop', 'sgd'
    LEARNING_RATE = 0.001  # 初始学习率
    
    # 评估指标
    METRICS = ['mae', 'mse']  # 训练时跟踪的指标


# ============================================
# 训练配置 / Training Configuration
# ============================================

class TrainingConfig:
    """模型训练配置"""
    
    # 基础训练参数
    EPOCHS = 100  # 最大训练轮数
    BATCH_SIZE = 32  # 批大小 (根据内存调整: 16, 32, 64, 128)
    VALIDATION_SPLIT = 0.0  # 不使用，我们手动划分了验证集
    SHUFFLE = False  # 时间序列数据不打乱顺序
    
    # 早停配置（Early Stopping）
    USE_EARLY_STOPPING = True  # 是否使用早停
    EARLY_STOPPING_PATIENCE = 15  # 多少个epoch没有改善就停止
    EARLY_STOPPING_MIN_DELTA = 0.0001  # 最小改善幅度
    EARLY_STOPPING_MONITOR = 'val_loss'  # 监控的指标
    RESTORE_BEST_WEIGHTS = True  # 恢复最佳权重
    
    # 学习率调整配置（ReduceLROnPlateau）
    USE_REDUCE_LR = True  # 是否使用学习率衰减
    REDUCE_LR_FACTOR = 0.5  # 学习率衰减因子
    REDUCE_LR_PATIENCE = 7  # 多少个epoch没有改善就降低学习率
    REDUCE_LR_MIN_LR = 1e-7  # 最小学习率
    REDUCE_LR_MONITOR = 'val_loss'  # 监控的指标
    
    # 模型检查点配置（ModelCheckpoint）
    USE_MODEL_CHECKPOINT = True  # 是否保存最佳模型
    CHECKPOINT_MONITOR = 'val_loss'  # 监控的指标
    CHECKPOINT_MODE = 'min'  # 'min' 表示指标越小越好
    CHECKPOINT_SAVE_BEST_ONLY = True  # 只保存最佳模型
    CHECKPOINT_SAVE_WEIGHTS_ONLY = False  # 保存完整模型
    
    # 训练日志配置
    VERBOSE = 1  # 训练时的输出详细程度: 0=静默, 1=进度条, 2=每个epoch一行
    USE_TENSORBOARD = False  # 是否使用TensorBoard (可选)
    
    # GPU配置
    USE_GPU = True  # 是否尝试使用GPU
    GPU_MEMORY_GROWTH = True  # 动态分配GPU内存
    MIXED_PRECISION = False  # 混合精度训练（需要GPU）


# ============================================
# 路径配置 / Path Configuration
# ============================================

class PathConfig:
    """文件路径配置"""
    
    # 基础目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    LSTM_DATA_DIR = os.path.join(BASE_DIR, 'lstm_data')
    MODELS_DIR = os.path.join(BASE_DIR, 'lstm_models')
    RESULTS_DIR = os.path.join(BASE_DIR, 'lstm_results')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # 模型保存路径
    MODEL_NAME = f'{DataConfig.SYMBOL}_lstm_model.h5'
    MODEL_PATH = os.path.join(MODELS_DIR, MODEL_NAME)
    CHECKPOINT_PATH = os.path.join(MODELS_DIR, f'{DataConfig.SYMBOL}_checkpoint.h5')
    
    # Scaler保存路径
    SCALER_PATH = os.path.join(MODELS_DIR, f'{DataConfig.SYMBOL}_scaler.pkl')
    
    # 结果保存路径
    TRAINING_HISTORY_PATH = os.path.join(RESULTS_DIR, 'training_history.csv')
    PREDICTIONS_PATH = os.path.join(RESULTS_DIR, 'predictions.csv')
    
    # 创建必要的目录
    @staticmethod
    def create_directories():
        """创建所有必要的目录"""
        for dir_path in [
            PathConfig.DATA_DIR,
            PathConfig.LSTM_DATA_DIR,
            PathConfig.MODELS_DIR,
            PathConfig.RESULTS_DIR,
            PathConfig.LOGS_DIR
        ]:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ 目录已创建/确认: {dir_path}")


# ============================================
# 预设配置方案 / Preset Configurations
# ============================================

class PresetConfigs:
    """预设的配置方案，方便快速切换"""
    
    @staticmethod
    def quick_test():
        """快速测试配置（小数据量，快速训练）"""
        DataConfig.LOOKBACK_DAYS = 90
        DataConfig.TIME_STEPS = 30
        ModelConfig.LSTM_UNITS = [64, 32]
        ModelConfig.DENSE_UNITS = [16]
        TrainingConfig.EPOCHS = 20
        TrainingConfig.BATCH_SIZE = 64
        TrainingConfig.EARLY_STOPPING_PATIENCE = 5
        print("✓ 已应用【快速测试】配置")
    
    @staticmethod
    def production():
        """生产环境配置（完整训练）"""
        DataConfig.LOOKBACK_DAYS = 730  # 2年数据
        DataConfig.TIME_STEPS = 60
        ModelConfig.LSTM_UNITS = [256, 128, 64]
        ModelConfig.DENSE_UNITS = [32, 16]
        TrainingConfig.EPOCHS = 200
        TrainingConfig.BATCH_SIZE = 32
        TrainingConfig.EARLY_STOPPING_PATIENCE = 20
        print("✓ 已应用【生产环境】配置")
    
    @staticmethod
    def gpu_optimized():
        """GPU优化配置（大批量）"""
        TrainingConfig.BATCH_SIZE = 128
        TrainingConfig.USE_GPU = True
        TrainingConfig.MIXED_PRECISION = True
        ModelConfig.LSTM_UNITS = [512, 256, 128]
        print("✓ 已应用【GPU优化】配置")
    
    @staticmethod
    def cpu_friendly():
        """CPU友好配置（小批量，简单模型）"""
        TrainingConfig.BATCH_SIZE = 16
        TrainingConfig.USE_GPU = False
        ModelConfig.LSTM_UNITS = [64, 32]
        ModelConfig.DENSE_UNITS = [16]
        TrainingConfig.EPOCHS = 50
        print("✓ 已应用【CPU友好】配置")


# ============================================
# 可视化配置 / Visualization Configuration
# ============================================

class VisualizationConfig:
    """可视化相关配置"""
    
    # 图表样式
    STYLE = 'seaborn-v0_8-darkgrid'  # matplotlib样式
    FIGURE_SIZE = (15, 8)  # 图表大小
    DPI = 100  # 图表分辨率
    
    # 颜色配置
    TRAIN_COLOR = '#1f77b4'  # 训练集颜色（蓝色）
    VAL_COLOR = '#ff7f0e'    # 验证集颜色（橙色）
    TEST_COLOR = '#2ca02c'   # 测试集颜色（绿色）
    PRED_COLOR = '#d62728'   # 预测颜色（红色）
    
    # 保存配置
    SAVE_PLOTS = True  # 是否保存图表
    PLOT_FORMAT = 'png'  # 图表格式: png, jpg, svg, pdf
    
    # 中文字体支持
    FONT_FAMILY = 'SimHei'  # 中文字体（黑体）
    FONT_SIZE = 12


# ============================================
# 日志配置 / Logging Configuration
# ============================================

class LogConfig:
    """日志配置"""
    
    # 日志级别
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # 日志格式
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # 日志文件
    LOG_FILE = os.path.join(PathConfig.LOGS_DIR, 'lstm_training.log')
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5  # 保留5个备份日志


# ============================================
# 辅助函数 / Helper Functions
# ============================================

def print_config_summary():
    """打印当前配置摘要"""
    print("=" * 60)
    print("LSTM 模型配置摘要 / LSTM Model Configuration Summary")
    print("=" * 60)
    print(f"\n📊 数据配置:")
    print(f"  - 交易对: {DataConfig.SYMBOL}")
    print(f"  - 时间间隔: {DataConfig.INTERVAL}")
    print(f"  - 历史数据: {DataConfig.LOOKBACK_DAYS} 天")
    print(f"  - 时间窗口: {DataConfig.TIME_STEPS} 个时间点")
    print(f"  - 数据划分: 训练{int(DataConfig.TRAIN_RATIO*100)}% / 验证{int(DataConfig.VAL_RATIO*100)}% / 测试{int(DataConfig.TEST_RATIO*100)}%")
    
    print(f"\n🧠 模型配置:")
    print(f"  - 模型类型: {ModelConfig.MODEL_TYPE}")
    print(f"  - LSTM层: {ModelConfig.LSTM_UNITS}")
    print(f"  - Dense层: {ModelConfig.DENSE_UNITS}")
    print(f"  - Dropout: {ModelConfig.DROPOUT_RATE}")
    print(f"  - 批标准化: {'启用' if ModelConfig.USE_BATCH_NORMALIZATION else '禁用'}")
    
    print(f"\n🏋️ 训练配置:")
    print(f"  - 最大轮数: {TrainingConfig.EPOCHS}")
    print(f"  - 批大小: {TrainingConfig.BATCH_SIZE}")
    print(f"  - 学习率: {ModelConfig.LEARNING_RATE}")
    print(f"  - 早停: {'启用' if TrainingConfig.USE_EARLY_STOPPING else '禁用'} (耐心值: {TrainingConfig.EARLY_STOPPING_PATIENCE})")
    print(f"  - 学习率衰减: {'启用' if TrainingConfig.USE_REDUCE_LR else '禁用'}")
    print(f"  - GPU加速: {'尝试启用' if TrainingConfig.USE_GPU else '禁用'}")
    
    print(f"\n📁 路径配置:")
    print(f"  - 模型保存: {PathConfig.MODEL_PATH}")
    print(f"  - 结果保存: {PathConfig.RESULTS_DIR}")
    print("=" * 60)


def get_input_shape(num_features: int) -> Tuple[int, int]:
    """
    获取LSTM输入形状
    
    Args:
        num_features: 特征数量
    
    Returns:
        (time_steps, num_features)
    """
    return (DataConfig.TIME_STEPS, num_features)


def estimate_training_time() -> str:
    """
    估算训练时间
    
    Returns:
        预估的训练时间字符串
    """
    # 粗略估算（基于经验）
    epochs = TrainingConfig.EPOCHS
    batch_size = TrainingConfig.BATCH_SIZE
    
    # CPU大约每个epoch 20-30秒，GPU大约5-10秒
    if TrainingConfig.USE_GPU:
        time_per_epoch = 7  # 秒
        device = "GPU"
    else:
        time_per_epoch = 25  # 秒
        device = "CPU"
    
    total_seconds = epochs * time_per_epoch
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    return f"预计 {minutes} 分 {seconds} 秒 ({device})"


if __name__ == "__main__":
    # 测试配置
    print_config_summary()
    print(f"\n⏱️ 预计训练时间: {estimate_training_time()}")
    print(f"\n✅ 配置文件加载成功！")
    
    # 创建必要的目录
    PathConfig.create_directories()
