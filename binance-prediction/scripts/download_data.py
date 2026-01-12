import os
import sys
import argparse

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.binance_client import BinanceUtility

def main():
    parser = argparse.ArgumentParser(description='Download Historical Data from Binance')
    parser.add_argument('--symbols', type=str, default='BTCUSDT,ETHUSDT', help='Comma separated symbols')
    parser.add_argument('--interval', type=str, default='1h', help='Time interval (1m, 5m, 1h, 1d)')
    parser.add_argument('--start', type=str, default='2 years ago UTC', help='Start time')
    
    args = parser.parse_args()
    symbols = args.symbols.split(',')
    
    client = BinanceUtility()
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    for symbol in symbols:
        symbol = symbol.strip()
        print(f"正在下载 {symbol}... / Downloading {symbol}...")
        df = client.fetch_historical_data(symbol, args.interval, args.start)
        if df is not None:
            file_path = f'data/{symbol}_hist.csv'
            df.to_csv(file_path, index=False)
            print(f"成功保存到 {file_path} / Successfully saved to {file_path}")
        else:
            print(f"下载 {symbol} 失败 / Failed to download {symbol}")

if __name__ == "__main__":
    main()
