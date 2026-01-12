"""
LSTM 模型构建模块
LSTM Model Builder Module

构建各种LSTM架构的模型
Build LSTM models with various architectures

作者: qinshihuang166
"""

import os
import sys
import numpy as np
from typing import Tuple, List, Optional

# TensorFlow imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    LSTM, Bidirectional, Dense, Dropout, 
    BatchNormalization, Input, Attention,
    Layer, LayerNormalization
)
from tensorflow.keras.regularizers import l1, l2, l1_l2
from tensorflow.keras.optimizers import Adam, RMSprop, SGD
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, 
    ReduceLROnPlateau, TensorBoard, Callback
)

# 导入配置
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_lstm import ModelConfig, TrainingConfig, PathConfig


class LSTMModelBuilder:
    """
    LSTM模型构建器
    
    支持多种架构:
    - 标准LSTM
    - 双向LSTM (BiLSTM)
    - 多层堆叠LSTM
    - 带Attention机制的LSTM
    """
    
    def __init__(self, config: Optional[ModelConfig] = None):
        """
        初始化模型构建器
        
        Args:
            config: 模型配置对象
        """
        self.config = config or ModelConfig()
        self.model = None
        
    def build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        根据配置构建LSTM模型
        
        Args:
            input_shape: 输入形状 (time_steps, features)
            
        Returns:
            编译好的Keras模型
        """
        print(f"\n🏗️ 开始构建LSTM模型...")
        print(f"  输入形状: {input_shape}")
        print(f"  模型类型: {self.config.MODEL_TYPE}")
        
        if self.config.MODEL_TYPE in ['LSTM', 'BiLSTM']:
            self.model = self._build_stacked_lstm(input_shape)
        elif self.config.MODEL_TYPE in ['GRU', 'BiGRU']:
            self.model = self._build_stacked_gru(input_shape)
        else:
            raise ValueError(f"不支持的模型类型: {self.config.MODEL_TYPE}")
        
        # 编译模型
        self._compile_model()
        
        # 打印模型摘要
        print("\n📋 模型架构摘要:")
        self.model.summary()
        
        # 计算参数数量
        total_params = self.model.count_params()
        print(f"\n📊 总参数数量: {total_params:,}")
        
        return self.model
    
    def _build_stacked_lstm(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        构建堆叠LSTM模型
        
        架构:
        Input → [LSTM → BatchNorm → Dropout] × N → Dense → Output
        
        Args:
            input_shape: (time_steps, features)
            
        Returns:
            Keras模型
        """
        model = Sequential(name='Stacked_LSTM')
        
        # 是否使用双向LSTM
        use_bidirectional = self.config.MODEL_TYPE == 'BiLSTM'
        
        # 获取正则化器
        regularizer = self._get_regularizer()
        
        # 第一层LSTM（需要指定input_shape）
        lstm_units = self.config.LSTM_UNITS
        
        for i, units in enumerate(lstm_units):
            # 判断是否是最后一层LSTM
            return_sequences = (i < len(lstm_units) - 1)
            
            # 创建LSTM层
            lstm_layer = LSTM(
                units=units,
                return_sequences=return_sequences,
                dropout=self.config.DROPOUT_RATE,
                recurrent_dropout=self.config.RECURRENT_DROPOUT,
                kernel_regularizer=regularizer,
                name=f'lstm_{i+1}'
            )
            
            # 是否使用双向
            if use_bidirectional:
                lstm_layer = Bidirectional(lstm_layer, name=f'bi_lstm_{i+1}')
            
            # 第一层需要指定输入形状
            if i == 0:
                model.add(Input(shape=input_shape, name='input'))
                model.add(lstm_layer)
            else:
                model.add(lstm_layer)
            
            # BatchNormalization
            if self.config.USE_BATCH_NORMALIZATION:
                model.add(BatchNormalization(name=f'batch_norm_{i+1}'))
            
            # Dropout（额外的Dropout层）
            if self.config.DROPOUT_RATE > 0 and return_sequences:
                model.add(Dropout(self.config.DROPOUT_RATE, name=f'dropout_{i+1}'))
        
        # Dense层
        for i, units in enumerate(self.config.DENSE_UNITS):
            model.add(Dense(
                units=units,
                activation=self.config.DENSE_ACTIVATION,
                kernel_regularizer=regularizer,
                name=f'dense_{i+1}'
            ))
            
            # BatchNormalization
            if self.config.USE_BATCH_NORMALIZATION:
                model.add(BatchNormalization(name=f'dense_batch_norm_{i+1}'))
            
            # Dropout
            if self.config.DROPOUT_RATE > 0:
                model.add(Dropout(self.config.DROPOUT_RATE, name=f'dense_dropout_{i+1}'))
        
        # 输出层
        model.add(Dense(
            units=1,
            activation=self.config.OUTPUT_ACTIVATION,
            name='output'
        ))
        
        return model
    
    def _build_stacked_gru(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        构建堆叠GRU模型（类似LSTM但更简单）
        
        Args:
            input_shape: (time_steps, features)
            
        Returns:
            Keras模型
        """
        from tensorflow.keras.layers import GRU
        
        model = Sequential(name='Stacked_GRU')
        
        use_bidirectional = self.config.MODEL_TYPE == 'BiGRU'
        regularizer = self._get_regularizer()
        
        gru_units = self.config.LSTM_UNITS  # 复用LSTM_UNITS配置
        
        for i, units in enumerate(gru_units):
            return_sequences = (i < len(gru_units) - 1)
            
            gru_layer = GRU(
                units=units,
                return_sequences=return_sequences,
                dropout=self.config.DROPOUT_RATE,
                recurrent_dropout=self.config.RECURRENT_DROPOUT,
                kernel_regularizer=regularizer,
                name=f'gru_{i+1}'
            )
            
            if use_bidirectional:
                gru_layer = Bidirectional(gru_layer, name=f'bi_gru_{i+1}')
            
            if i == 0:
                model.add(Input(shape=input_shape, name='input'))
                model.add(gru_layer)
            else:
                model.add(gru_layer)
            
            if self.config.USE_BATCH_NORMALIZATION:
                model.add(BatchNormalization(name=f'batch_norm_{i+1}'))
            
            if self.config.DROPOUT_RATE > 0 and return_sequences:
                model.add(Dropout(self.config.DROPOUT_RATE, name=f'dropout_{i+1}'))
        
        # Dense层
        for i, units in enumerate(self.config.DENSE_UNITS):
            model.add(Dense(
                units=units,
                activation=self.config.DENSE_ACTIVATION,
                kernel_regularizer=regularizer,
                name=f'dense_{i+1}'
            ))
            
            if self.config.USE_BATCH_NORMALIZATION:
                model.add(BatchNormalization(name=f'dense_batch_norm_{i+1}'))
            
            if self.config.DROPOUT_RATE > 0:
                model.add(Dropout(self.config.DROPOUT_RATE, name=f'dense_dropout_{i+1}'))
        
        # 输出层
        model.add(Dense(units=1, activation=self.config.OUTPUT_ACTIVATION, name='output'))
        
        return model
    
    def _get_regularizer(self):
        """获取正则化器"""
        if self.config.USE_L1_REGULARIZATION and self.config.USE_L2_REGULARIZATION:
            return l1_l2(l1=self.config.L1_LAMBDA, l2=self.config.L2_LAMBDA)
        elif self.config.USE_L1_REGULARIZATION:
            return l1(self.config.L1_LAMBDA)
        elif self.config.USE_L2_REGULARIZATION:
            return l2(self.config.L2_LAMBDA)
        else:
            return None
    
    def _compile_model(self):
        """编译模型"""
        print(f"\n⚙️ 编译模型...")
        
        # 选择优化器
        if self.config.OPTIMIZER == 'adam':
            optimizer = Adam(learning_rate=self.config.LEARNING_RATE)
        elif self.config.OPTIMIZER == 'rmsprop':
            optimizer = RMSprop(learning_rate=self.config.LEARNING_RATE)
        elif self.config.OPTIMIZER == 'sgd':
            optimizer = SGD(learning_rate=self.config.LEARNING_RATE)
        else:
            raise ValueError(f"不支持的优化器: {self.config.OPTIMIZER}")
        
        # 编译
        self.model.compile(
            optimizer=optimizer,
            loss=self.config.LOSS_FUNCTION,
            metrics=self.config.METRICS
        )
        
        print(f"  ✓ 优化器: {self.config.OPTIMIZER}")
        print(f"  ✓ 学习率: {self.config.LEARNING_RATE}")
        print(f"  ✓ 损失函数: {self.config.LOSS_FUNCTION}")
        print(f"  ✓ 评估指标: {self.config.METRICS}")
    
    def get_callbacks(self) -> List[Callback]:
        """
        获取训练回调函数
        
        Returns:
            回调函数列表
        """
        callbacks = []
        train_config = TrainingConfig()
        
        # 1. EarlyStopping
        if train_config.USE_EARLY_STOPPING:
            early_stopping = EarlyStopping(
                monitor=train_config.EARLY_STOPPING_MONITOR,
                patience=train_config.EARLY_STOPPING_PATIENCE,
                min_delta=train_config.EARLY_STOPPING_MIN_DELTA,
                restore_best_weights=train_config.RESTORE_BEST_WEIGHTS,
                verbose=1
            )
            callbacks.append(early_stopping)
            print(f"  ✓ EarlyStopping (耐心值: {train_config.EARLY_STOPPING_PATIENCE})")
        
        # 2. ReduceLROnPlateau
        if train_config.USE_REDUCE_LR:
            reduce_lr = ReduceLROnPlateau(
                monitor=train_config.REDUCE_LR_MONITOR,
                factor=train_config.REDUCE_LR_FACTOR,
                patience=train_config.REDUCE_LR_PATIENCE,
                min_lr=train_config.REDUCE_LR_MIN_LR,
                verbose=1
            )
            callbacks.append(reduce_lr)
            print(f"  ✓ ReduceLROnPlateau (因子: {train_config.REDUCE_LR_FACTOR})")
        
        # 3. ModelCheckpoint
        if train_config.USE_MODEL_CHECKPOINT:
            # 确保目录存在
            os.makedirs(os.path.dirname(PathConfig.CHECKPOINT_PATH), exist_ok=True)
            
            checkpoint = ModelCheckpoint(
                filepath=PathConfig.CHECKPOINT_PATH,
                monitor=train_config.CHECKPOINT_MONITOR,
                mode=train_config.CHECKPOINT_MODE,
                save_best_only=train_config.CHECKPOINT_SAVE_BEST_ONLY,
                save_weights_only=train_config.CHECKPOINT_SAVE_WEIGHTS_ONLY,
                verbose=1
            )
            callbacks.append(checkpoint)
            print(f"  ✓ ModelCheckpoint (保存路径: {PathConfig.CHECKPOINT_PATH})")
        
        # 4. TensorBoard (可选)
        if train_config.USE_TENSORBOARD:
            log_dir = os.path.join(PathConfig.LOGS_DIR, 'tensorboard')
            os.makedirs(log_dir, exist_ok=True)
            
            tensorboard = TensorBoard(
                log_dir=log_dir,
                histogram_freq=1,
                write_graph=True
            )
            callbacks.append(tensorboard)
            print(f"  ✓ TensorBoard (日志目录: {log_dir})")
        
        # 5. 自定义进度回调
        progress_callback = TrainingProgressCallback()
        callbacks.append(progress_callback)
        print(f"  ✓ TrainingProgressCallback (训练进度显示)")
        
        return callbacks
    
    def save_model(self, path: Optional[str] = None):
        """保存模型"""
        if self.model is None:
            raise ValueError("❌ 模型尚未构建")
        
        path = path or PathConfig.MODEL_PATH
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        self.model.save(path)
        print(f"✅ 模型已保存: {path}")
    
    def load_model(self, path: Optional[str] = None) -> keras.Model:
        """加载模型"""
        path = path or PathConfig.MODEL_PATH
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ 模型文件不存在: {path}")
        
        self.model = keras.models.load_model(path)
        print(f"✅ 模型已加载: {path}")
        
        return self.model


class TrainingProgressCallback(Callback):
    """自定义训练进度回调"""
    
    def __init__(self):
        super().__init__()
        self.epoch_start_time = None
    
    def on_train_begin(self, logs=None):
        print("\n" + "="*60)
        print("🚀 开始训练模型...")
        print("="*60)
    
    def on_epoch_begin(self, epoch, logs=None):
        import time
        self.epoch_start_time = time.time()
    
    def on_epoch_end(self, epoch, logs=None):
        import time
        epoch_time = time.time() - self.epoch_start_time
        
        # 获取指标
        loss = logs.get('loss', 0)
        val_loss = logs.get('val_loss', 0)
        mae = logs.get('mae', 0)
        val_mae = logs.get('val_mae', 0)
        
        # 打印进度
        print(f"\n📊 Epoch {epoch + 1} 完成 (用时: {epoch_time:.2f}秒)")
        print(f"  训练集 - Loss: {loss:.6f}, MAE: {mae:.6f}")
        print(f"  验证集 - Loss: {val_loss:.6f}, MAE: {val_mae:.6f}")
        
        # 学习率
        lr = self.model.optimizer.learning_rate
        if hasattr(lr, 'numpy'):
            lr_value = lr.numpy()
            print(f"  当前学习率: {lr_value:.2e}")
    
    def on_train_end(self, logs=None):
        print("\n" + "="*60)
        print("✅ 训练完成!")
        print("="*60)


def setup_gpu():
    """配置GPU"""
    train_config = TrainingConfig()
    
    if not train_config.USE_GPU:
        # 禁用GPU
        tf.config.set_visible_devices([], 'GPU')
        print("💻 使用 CPU 训练")
        return False
    
    # 检查GPU是否可用
    gpus = tf.config.list_physical_devices('GPU')
    
    if len(gpus) == 0:
        print("⚠️ 未检测到GPU，使用CPU训练")
        return False
    
    print(f"🎮 检测到 {len(gpus)} 个GPU: {gpus}")
    
    # 配置GPU内存增长
    if train_config.GPU_MEMORY_GROWTH:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("  ✓ GPU内存动态增长已启用")
        except RuntimeError as e:
            print(f"  ⚠️ 设置GPU内存增长失败: {e}")
    
    # 混合精度训练
    if train_config.MIXED_PRECISION:
        try:
            from tensorflow.keras import mixed_precision
            policy = mixed_precision.Policy('mixed_float16')
            mixed_precision.set_global_policy(policy)
            print("  ✓ 混合精度训练已启用 (FP16)")
        except Exception as e:
            print(f"  ⚠️ 启用混合精度失败: {e}")
    
    return True


def test_model_builder():
    """测试模型构建器"""
    print("LSTM模型构建器测试\n")
    
    # 配置GPU
    has_gpu = setup_gpu()
    
    # 创建模型构建器
    builder = LSTMModelBuilder()
    
    # 构建模型
    input_shape = (60, 20)  # (time_steps, features)
    model = builder.build_model(input_shape)
    
    # 创建虚拟数据测试
    X_dummy = np.random.randn(100, 60, 20).astype(np.float32)
    y_dummy = np.random.randn(100, 1).astype(np.float32)
    
    print("\n🧪 测试前向传播...")
    predictions = model.predict(X_dummy[:10], verbose=0)
    print(f"  ✓ 预测形状: {predictions.shape}")
    print(f"  ✓ 预测值示例: {predictions[:3].flatten()}")
    
    print("\n✅ 测试完成!")


if __name__ == "__main__":
    test_model_builder()
