import os
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
import argparse

# 将项目根目录添加到路径
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.binance_client import BinanceUtility
from utils.data_processor import DataProcessor

def main(args):
    # 1. 获取数据
    # 1. Fetch Data
    if args.local_data and os.path.exists(args.local_data):
        print(f"加载本地数据: {args.local_data} / Loading local data: {args.local_data}")
        df = pd.read_csv(args.local_data)
    else:
        print(f"从 Binance 获取数据 for {args.symbol}...")
        client = BinanceUtility()
        df = client.fetch_historical_data(args.symbol, '1h', '1 year ago UTC')
        # 保存原始数据
        if not os.path.exists('data'): os.makedirs('data')
        df.to_csv(f'data/{args.symbol}_hist.csv', index=False)

    # 2. 处理数据
    # 2. Process Data
    print("正在进行特征工程... / Feature engineering...")
    processor = DataProcessor()
    df_with_features = processor.add_technical_indicators(df)
    X, y = processor.prepare_features_labels(df_with_features)

    # 3. 划分训练集和测试集
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # 4. 训练模型
    # 4. Train Model
    print("正在训练随机森林模型... / Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. 评估模型
    # 5. Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n模型准确率: {accuracy:.4f} / Model Accuracy: {accuracy:.4f}")
    print("\n分类报告 / Classification Report:")
    print(classification_report(y_test, y_pred))

    # 交叉验证
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"\n5折交叉验证平均分: {cv_scores.mean():.4f} / 5-Fold CV Mean Score: {cv_scores.mean():.4f}")

    # 6. 保存模型
    # 6. Save Model
    if not os.path.exists('models'): os.makedirs('models')
    model_path = f'models/{args.symbol}_price_model.pkl'
    joblib.dump(model, model_path)
    print(f"\n模型已保存至: {model_path} / Model saved to: {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binance Price Prediction Model Training')
    parser.add_argument('--symbol', type=str, default='BTCUSDT', help='Trading pair symbol')
    parser.add_argument('--local_data', type=str, default=None, help='Path to local CSV data file')
    
    args = parser.parse_args()
    main(args)
