"""
LSTM数据下载脚本
LSTM Data Download Script

从Binance下载训练LSTM所需的历史数据
Download historical data from Binance for LSTM training

作者: qinshihuang166
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.binance_client import BinanceUtility
from config_lstm import DataConfig, PathConfig


def download_data(symbol: str = None, 
                 interval: str = None, 
                 days: int = None,
                 save_path: str = None):
    """
    下载历史数据
    
    Args:
        symbol: 交易对符号
        interval: 时间间隔
        days: 回溯天数
        save_path: 保存路径
    """
    # 使用配置或参数
    symbol = symbol or DataConfig.SYMBOL
    interval = interval or DataConfig.INTERVAL
    days = days or DataConfig.LOOKBACK_DAYS
    
    print("="*60)
    print("📥 Binance 数据下载器")
    print("="*60)
    print(f"交易对: {symbol}")
    print(f"时间间隔: {interval}")
    print(f"回溯天数: {days} 天")
    print("="*60)
    
    # 初始化Binance客户端
    try:
        client = BinanceUtility()
    except Exception as e:
        print(f"❌ 初始化Binance客户端失败: {e}")
        print("\n💡 提示: 如果没有API密钥，可以使用公开API（有请求限制）")
        print("   在项目根目录创建 .env 文件，添加:")
        print("   BINANCE_API_KEY=your_key")
        print("   BINANCE_API_SECRET=your_secret")
        return False
    
    # 计算开始时间
    start_date = datetime.now() - timedelta(days=days)
    start_str = start_date.strftime("%d %b, %Y")
    
    print(f"\n⏳ 开始下载数据 (从 {start_str} 至今)...")
    print("这可能需要几分钟时间，请耐心等待...\n")
    
    # 下载数据
    try:
        df = client.fetch_historical_data(
            symbol=symbol,
            interval=interval,
            start_str=start_str
        )
        
        if df is None or df.empty:
            print("❌ 下载失败或数据为空")
            return False
        
        # 数据验证
        print(f"\n✅ 数据下载成功!")
        print(f"  数据行数: {len(df)}")
        print(f"  时间范围: {df['timestamp'].min()} 到 {df['timestamp'].max()}")
        print(f"  列名: {list(df.columns)}")
        
        # 数据统计
        print(f"\n📊 数据统计:")
        print(f"  开盘价范围: {df['open'].min():.2f} - {df['open'].max():.2f}")
        print(f"  收盘价范围: {df['close'].min():.2f} - {df['close'].max():.2f}")
        print(f"  成交量范围: {df['volume'].min():.2f} - {df['volume'].max():.2f}")
        
        # 保存数据
        PathConfig.create_directories()
        save_path = save_path or DataConfig.RAW_DATA_FILE
        df.to_csv(save_path, index=False)
        
        print(f"\n💾 数据已保存到: {save_path}")
        print(f"   文件大小: {os.path.getsize(save_path) / 1024:.2f} KB")
        
        # 显示前几行数据
        print(f"\n📋 数据预览 (前5行):")
        print(df.head())
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def download_multiple_symbols(symbols: list, 
                             interval: str = None, 
                             days: int = None):
    """
    下载多个交易对的数据
    
    Args:
        symbols: 交易对列表
        interval: 时间间隔
        days: 回溯天数
    """
    results = {}
    
    print("="*60)
    print(f"📥 批量下载 {len(symbols)} 个交易对的数据")
    print("="*60)
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] 下载 {symbol}...")
        
        # 生成保存路径
        save_path = os.path.join(DataConfig.DATA_DIR, f'{symbol}_raw_data.csv')
        
        # 下载
        success = download_data(
            symbol=symbol,
            interval=interval,
            days=days,
            save_path=save_path
        )
        
        results[symbol] = success
    
    # 打印汇总
    print("\n" + "="*60)
    print("📊 下载结果汇总")
    print("="*60)
    
    success_count = sum(results.values())
    for symbol, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{symbol}: {status}")
    
    print(f"\n总计: {success_count}/{len(symbols)} 成功")
    print("="*60)


def validate_existing_data():
    """验证已存在的数据"""
    data_file = DataConfig.RAW_DATA_FILE
    
    if not os.path.exists(data_file):
        print(f"❌ 数据文件不存在: {data_file}")
        print("请先运行下载命令！")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(data_file)
        
        print("="*60)
        print("✅ 数据文件验证")
        print("="*60)
        print(f"文件路径: {data_file}")
        print(f"文件大小: {os.path.getsize(data_file) / 1024:.2f} KB")
        print(f"数据行数: {len(df)}")
        print(f"数据列数: {len(df.columns)}")
        print(f"列名: {list(df.columns)}")
        
        # 检查必需列
        required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\n⚠️ 缺少必需列: {missing_cols}")
            return False
        else:
            print(f"\n✅ 所有必需列都存在")
        
        # 数据统计
        print(f"\n📊 数据统计:")
        print(df.describe())
        
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='从Binance下载历史数据用于LSTM训练',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用默认配置下载
  python download_lstm_data.py
  
  # 自定义参数
  python download_lstm_data.py --symbol ETHUSDT --interval 4h --days 730
  
  # 下载多个交易对
  python download_lstm_data.py --symbols BTCUSDT,ETHUSDT,BNBUSDT --days 365
  
  # 验证已存在的数据
  python download_lstm_data.py --validate
        """
    )
    
    parser.add_argument(
        '--symbol', 
        type=str, 
        default=None,
        help=f'交易对符号 (默认: {DataConfig.SYMBOL})'
    )
    
    parser.add_argument(
        '--symbols',
        type=str,
        default=None,
        help='多个交易对，用逗号分隔 (例如: BTCUSDT,ETHUSDT)'
    )
    
    parser.add_argument(
        '--interval', 
        type=str, 
        default=None,
        help=f'时间间隔: 1m, 5m, 15m, 1h, 4h, 1d (默认: {DataConfig.INTERVAL})'
    )
    
    parser.add_argument(
        '--days', 
        type=int, 
        default=None,
        help=f'回溯天数 (默认: {DataConfig.LOOKBACK_DAYS})'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='验证已存在的数据文件'
    )
    
    args = parser.parse_args()
    
    # 验证模式
    if args.validate:
        validate_existing_data()
        return
    
    # 批量下载模式
    if args.symbols:
        symbols = [s.strip() for s in args.symbols.split(',')]
        download_multiple_symbols(
            symbols=symbols,
            interval=args.interval,
            days=args.days
        )
        return
    
    # 单个下载模式
    success = download_data(
        symbol=args.symbol,
        interval=args.interval,
        days=args.days
    )
    
    if success:
        print("\n" + "="*60)
        print("🎉 数据下载完成!")
        print("="*60)
        print("\n下一步:")
        print("  1. 运行 train_lstm.py 开始训练模型")
        print("  2. 或查看教程笔记本了解LSTM原理")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ 数据下载失败，请检查错误信息")
        print("="*60)


if __name__ == "__main__":
    main()
