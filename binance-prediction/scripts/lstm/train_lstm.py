"""
LSTM模型训练脚本
LSTM Model Training Script

完整的LSTM模型训练流程
Complete LSTM model training pipeline

作者: qinshihuang166
使用方法:
    python train_lstm.py                    # 使用默认配置训练
    python train_lstm.py --quick-test       # 快速测试模式
    python train_lstm.py --symbol ETHUSDT   # 指定交易对
"""

import os
import sys
import argparse
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入模块
from config_lstm import (
    DataConfig, ModelConfig, TrainingConfig, PathConfig,
    PresetConfigs, print_config_summary, estimate_training_time
)
from utils.lstm_data_processor import LSTMDataProcessor
from utils.lstm_model_builder import LSTMModelBuilder, setup_gpu
import pandas as pd
import numpy as np


def train_model(args):
    """
    主训练函数
    
    Args:
        args: 命令行参数
    """
    start_time = time.time()
    
    # ============================================
    # 1. 应用配置
    # ============================================
    print("="*70)
    print(" "*20 + "🚀 LSTM 价格预测模型训练")
    print("="*70)
    
    # 应用预设配置
    if args.quick_test:
        print("\n⚡ 应用快速测试配置...")
        PresetConfigs.quick_test()
    elif args.production:
        print("\n🏭 应用生产环境配置...")
        PresetConfigs.production()
    elif args.gpu_optimized:
        print("\n🎮 应用GPU优化配置...")
        PresetConfigs.gpu_optimized()
    elif args.cpu_friendly:
        print("\n💻 应用CPU友好配置...")
        PresetConfigs.cpu_friendly()
    
    # 自定义配置覆盖
    if args.symbol:
        DataConfig.SYMBOL = args.symbol
    if args.epochs:
        TrainingConfig.EPOCHS = args.epochs
    if args.batch_size:
        TrainingConfig.BATCH_SIZE = args.batch_size
    
    # 打印配置摘要
    print_config_summary()
    print(f"\n⏱️ {estimate_training_time()}\n")
    
    # 创建必要的目录
    PathConfig.create_directories()
    
    # ============================================
    # 2. 配置GPU/CPU
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 1: 配置计算设备")
    print("="*70)
    
    has_gpu = setup_gpu()
    
    if not has_gpu and args.gpu_optimized:
        print("\n⚠️ 警告: 请求GPU优化但未检测到GPU，将使用CPU")
        PresetConfigs.cpu_friendly()
    
    # ============================================
    # 3. 数据处理
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 2: 数据处理")
    print("="*70)
    
    # 检查数据文件是否存在
    if not os.path.exists(DataConfig.RAW_DATA_FILE):
        print(f"\n❌ 错误: 数据文件不存在: {DataConfig.RAW_DATA_FILE}")
        print("\n💡 解决方案:")
        print("   1. 运行数据下载脚本:")
        print(f"      python scripts/lstm/download_lstm_data.py")
        print("\n   2. 或者手动下载数据并放到 data/ 目录")
        print(f"      文件名应为: {os.path.basename(DataConfig.RAW_DATA_FILE)}")
        sys.exit(1)
    
    # 创建数据处理器
    processor = LSTMDataProcessor()
    
    try:
        # 执行完整的数据处理流程
        X_train, X_val, X_test, y_train, y_val, y_test = processor.process_all()
        
        print(f"\n✅ 数据处理完成!")
        print(f"  训练集: X={X_train.shape}, y={y_train.shape}")
        print(f"  验证集: X={X_val.shape}, y={y_val.shape}")
        print(f"  测试集: X={X_test.shape}, y={y_test.shape}")
        
    except Exception as e:
        print(f"\n❌ 数据处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # ============================================
    # 4. 构建模型
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 3: 构建LSTM模型")
    print("="*70)
    
    # 获取输入形状
    input_shape = (X_train.shape[1], X_train.shape[2])
    
    # 创建模型构建器
    model_builder = LSTMModelBuilder()
    
    try:
        # 构建模型
        model = model_builder.build_model(input_shape)
        
    except Exception as e:
        print(f"\n❌ 模型构建失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # ============================================
    # 5. 训练模型
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 4: 训练模型")
    print("="*70)
    
    # 获取回调函数
    print("\n📋 配置训练回调:")
    callbacks = model_builder.get_callbacks()
    
    # 开始训练
    try:
        print(f"\n⏰ 训练开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=TrainingConfig.EPOCHS,
            batch_size=TrainingConfig.BATCH_SIZE,
            callbacks=callbacks,
            verbose=TrainingConfig.VERBOSE,
            shuffle=TrainingConfig.SHUFFLE
        )
        
        print(f"\n⏰ 训练结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 训练被用户中断!")
        print("  已保存的最佳模型可以在 lstm_models/ 目录找到")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ 训练过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # ============================================
    # 6. 保存模型和结果
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 5: 保存模型和结果")
    print("="*70)
    
    # 保存最终模型
    model_builder.save_model()
    
    # 保存训练历史
    history_df = pd.DataFrame(history.history)
    history_df.to_csv(PathConfig.TRAINING_HISTORY_PATH, index=False)
    print(f"✓ 训练历史已保存: {PathConfig.TRAINING_HISTORY_PATH}")
    
    # ============================================
    # 7. 评估模型
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 6: 评估模型性能")
    print("="*70)
    
    # 在测试集上评估
    print("\n📊 测试集评估:")
    test_results = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"  Loss (MSE): {test_results[0]:.6f}")
    print(f"  MAE: {test_results[1]:.6f}")
    print(f"  MSE: {test_results[2]:.6f}")
    
    # 计算RMSE
    rmse = np.sqrt(test_results[0])
    print(f"  RMSE: {rmse:.6f}")
    
    # ============================================
    # 8. 可视化结果
    # ============================================
    print("\n" + "="*70)
    print("⚙️ 步骤 7: 生成可视化结果")
    print("="*70)
    
    try:
        visualize_results(model, history, X_train, y_train, X_val, y_val, X_test, y_test, processor)
    except Exception as e:
        print(f"⚠️ 可视化生成失败 (这不影响模型训练): {e}")
    
    # ============================================
    # 9. 总结
    # ============================================
    total_time = time.time() - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    print("\n" + "="*70)
    print("✅ 训练完成!")
    print("="*70)
    print(f"\n📊 训练总结:")
    print(f"  总用时: {minutes} 分 {seconds} 秒")
    print(f"  训练轮数: {len(history.history['loss'])} / {TrainingConfig.EPOCHS}")
    print(f"  最佳验证Loss: {min(history.history['val_loss']):.6f}")
    print(f"  测试集Loss: {test_results[0]:.6f}")
    print(f"  测试集RMSE: {rmse:.6f}")
    
    print(f"\n📁 输出文件:")
    print(f"  模型文件: {PathConfig.MODEL_PATH}")
    print(f"  检查点: {PathConfig.CHECKPOINT_PATH}")
    print(f"  Scaler: {PathConfig.SCALER_PATH}")
    print(f"  训练历史: {PathConfig.TRAINING_HISTORY_PATH}")
    print(f"  可视化结果: {PathConfig.RESULTS_DIR}/")
    
    print(f"\n🎯 下一步:")
    print(f"  1. 查看可视化结果: ls {PathConfig.RESULTS_DIR}/")
    print(f"  2. 进行预测: python scripts/lstm/predict_lstm.py")
    print(f"  3. 回测模型: python scripts/lstm/backtest_lstm.py")
    
    print("\n" + "="*70)


def visualize_results(model, history, X_train, y_train, X_val, y_val, X_test, y_test, processor):
    """
    生成可视化结果
    """
    import matplotlib
    matplotlib.use('Agg')  # 非GUI后端
    import matplotlib.pyplot as plt
    
    # 设置中文字体
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        pass
    
    results_dir = PathConfig.RESULTS_DIR
    
    # 1. 训练历史曲线
    print("\n  📈 生成训练历史曲线...")
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    # Loss曲线
    axes[0].plot(history.history['loss'], label='训练集 Loss', linewidth=2)
    axes[0].plot(history.history['val_loss'], label='验证集 Loss', linewidth=2)
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss (MSE)')
    axes[0].set_title('模型训练Loss曲线')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # MAE曲线
    axes[1].plot(history.history['mae'], label='训练集 MAE', linewidth=2)
    axes[1].plot(history.history['val_mae'], label='验证集 MAE', linewidth=2)
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('MAE')
    axes[1].set_title('模型训练MAE曲线')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'training_history.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 已保存: training_history.png")
    
    # 2. 预测 vs 实际值
    print("\n  📊 生成预测对比图...")
    
    # 在测试集上预测
    y_pred = model.predict(X_test, verbose=0).flatten()
    
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # 只显示前500个点（避免图表过于拥挤）
    display_points = min(500, len(y_test))
    x_range = range(display_points)
    
    ax.plot(x_range, y_test[:display_points], label='实际价格', linewidth=2, alpha=0.7)
    ax.plot(x_range, y_pred[:display_points], label='预测价格', linewidth=2, alpha=0.7)
    ax.set_xlabel('时间步')
    ax.set_ylabel('归一化价格')
    ax.set_title(f'LSTM预测 vs 实际价格 (测试集前{display_points}个点)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'prediction_vs_actual.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 已保存: prediction_vs_actual.png")
    
    # 3. 误差分布图
    print("\n  📉 生成误差分布图...")
    
    errors = y_test - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # 误差直方图
    axes[0].hist(errors, bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('预测误差')
    axes[0].set_ylabel('频数')
    axes[0].set_title('预测误差分布')
    axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='零误差线')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 误差散点图
    axes[1].scatter(y_test, y_pred, alpha=0.5, s=10)
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                 'r--', linewidth=2, label='完美预测线')
    axes[1].set_xlabel('实际值')
    axes[1].set_ylabel('预测值')
    axes[1].set_title('预测值 vs 实际值散点图')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'error_analysis.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    ✓ 已保存: error_analysis.png")
    
    # 4. 保存预测结果到CSV
    print("\n  💾 保存预测结果...")
    predictions_df = pd.DataFrame({
        'actual': y_test,
        'predicted': y_pred,
        'error': errors,
        'abs_error': np.abs(errors)
    })
    predictions_df.to_csv(PathConfig.PREDICTIONS_PATH, index=False)
    print(f"    ✓ 已保存: {PathConfig.PREDICTIONS_PATH}")
    
    print("\n✅ 可视化完成!")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='LSTM价格预测模型训练脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 默认配置训练
  python train_lstm.py
  
  # 快速测试（小数据量，快速完成）
  python train_lstm.py --quick-test
  
  # 生产环境配置（完整训练）
  python train_lstm.py --production
  
  # GPU优化配置
  python train_lstm.py --gpu-optimized
  
  # CPU友好配置
  python train_lstm.py --cpu-friendly
  
  # 自定义参数
  python train_lstm.py --symbol ETHUSDT --epochs 50 --batch-size 64
  
提示:
  - 首次训练建议使用 --quick-test 快速验证流程
  - 确保已下载数据: python scripts/lstm/download_lstm_data.py
  - 训练过程可以随时按 Ctrl+C 中断，最佳模型已保存
        """
    )
    
    # 预设配置组
    preset_group = parser.add_argument_group('预设配置（互斥）')
    presets = preset_group.add_mutually_exclusive_group()
    presets.add_argument('--quick-test', action='store_true', 
                        help='快速测试配置（小数据，快速训练）')
    presets.add_argument('--production', action='store_true',
                        help='生产环境配置（完整训练）')
    presets.add_argument('--gpu-optimized', action='store_true',
                        help='GPU优化配置（大批量）')
    presets.add_argument('--cpu-friendly', action='store_true',
                        help='CPU友好配置（小批量，简单模型）')
    
    # 自定义参数
    custom_group = parser.add_argument_group('自定义参数')
    custom_group.add_argument('--symbol', type=str, help='交易对符号')
    custom_group.add_argument('--epochs', type=int, help='训练轮数')
    custom_group.add_argument('--batch-size', type=int, help='批大小')
    
    args = parser.parse_args()
    
    # 开始训练
    train_model(args)


if __name__ == "__main__":
    main()
