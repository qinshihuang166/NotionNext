"""
数据可视化工具类 / Data Visualization Utility Class
This module provides various plotting functions to visualize cryptocurrency data and predictions
此模块提供多种绘图功能，用于可视化加密货币数据和预测结果
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style for better looking plots
# 设置图表样式
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class DataVisualizer:
    """
    数据可视化类 / Data Visualization Class
    Provides methods to create various types of charts for analysis
    提供创建各种分析图表的方法
    """
    
    @staticmethod
    def plot_price_history(df, title="Price History", figsize=(12, 6)):
        """
        绘制价格历史图 / Plot price history
        
        Parameters:
        -----------
        df : DataFrame
            Data must contain 'timestamp' and 'close' columns
            数据必须包含 'timestamp' 和 'close' 列
        title : str
            Chart title / 图表标题
        figsize : tuple
            Figure size / 图表尺寸
        """
        plt.figure(figsize=figsize)
        plt.plot(df['timestamp'], df['close'], label='Close Price', linewidth=1.5, color='blue')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Time / 时间', fontsize=12)
        plt.ylabel('Price (USDT)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_technical_indicators(df, indicators=['sma_7', 'sma_25'], figsize=(12, 6)):
        """
        绘制技术指标图 / Plot technical indicators
        
        Parameters:
        -----------
        df : DataFrame
            Data with price and technical indicators
            包含价格和技术指标的数据
        indicators : list
            List of indicator column names to plot
            要绘制的指标列名列表
        figsize : tuple
            Figure size / 图表尺寸
        """
        plt.figure(figsize=figsize)
        
        # Plot price / 绘制价格
        plt.plot(df['timestamp'], df['close'], label='Close Price', linewidth=1.5, color='black', alpha=0.7)
        
        # Plot indicators / 绘制指标
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        for i, indicator in enumerate(indicators):
            if indicator in df.columns:
                plt.plot(df['timestamp'], df[indicator], 
                        label=indicator.upper(), 
                        linewidth=1.5, 
                        color=colors[i % len(colors)])
        
        plt.title('Technical Indicators / 技术指标', fontsize=14, fontweight='bold')
        plt.xlabel('Time / 时间', fontsize=12)
        plt.ylabel('Price / 价格', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_rsi(df, window=14, figsize=(12, 6)):
        """
        绘制RSI指标图 / Plot RSI indicator
        
        Parameters:
        -----------
        df : DataFrame
            Data with RSI column
            包含RSI列的数据
        window : int
            RSI window size / RSI窗口大小
        figsize : tuple
            Figure size / 图表尺寸
        """
        plt.figure(figsize=figsize)
        
        if 'rsi_14' in df.columns:
            plt.plot(df['timestamp'], df['rsi_14'], label='RSI', linewidth=1.5, color='purple')
            
            # Add overbought and oversold lines / 添加超买和超卖线
            plt.axhline(y=70, color='r', linestyle='--', linewidth=1, label='Overbought (70) / 超买')
            plt.axhline(y=30, color='g', linestyle='--', linewidth=1, label='Oversold (30) / 超卖')
            
            plt.title(f'RSI ({window} periods) / 相对强弱指数', fontsize=14, fontweight='bold')
            plt.xlabel('Time / 时间', fontsize=12)
            plt.ylabel('RSI Value', fontsize=12)
            plt.legend(loc='best')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        else:
            print("RSI column not found in DataFrame / 数据框中未找到RSI列")
    
    @staticmethod
    def plot_predictions(df, predictions, title="Predictions vs Actual", figsize=(12, 6)):
        """
        绘制预测结果对比图 / Plot predictions vs actual prices
        
        Parameters:
        -----------
        df : DataFrame
            Data with actual prices
            包含实际价格的数据
        predictions : array
            Predicted values
            预测值
        title : str
            Chart title / 图表标题
        figsize : tuple
            Figure size / 图表尺寸
        """
        plt.figure(figsize=figsize)
        
        # Plot actual prices / 绘制实际价格
        plt.plot(df['close'].values, label='Actual Price / 实际价格', linewidth=2, color='blue', alpha=0.7)
        
        # Plot predictions / 绘制预测
        plt.plot(predictions, label='Predicted Price / 预测价格', linewidth=2, color='red', linestyle='--')
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Time Steps / 时间步', fontsize=12)
        plt.ylabel('Price (USDT)', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_feature_importance(model, feature_names, top_n=10, figsize=(10, 6)):
        """
        绘制特征重要性图 / Plot feature importance
        
        Parameters:
        -----------
        model : sklearn model
            Trained model with feature_importances_ attribute
            具有 feature_importances_ 属性的训练好的模型
        feature_names : list
            List of feature names
            特征名称列表
        top_n : int
            Number of top features to display
            显示的前N个重要特征
        figsize : tuple
            Figure size / 图表尺寸
        """
        if hasattr(model, 'feature_importances_'):
            # Get feature importances / 获取特征重要性
            importances = model.feature_importances_
            
            # Create DataFrame for easier plotting / 创建数据框以便绘图
            feature_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            })
            
            # Sort by importance and get top N / 按重要性排序并获取前N个
            feature_df = feature_df.sort_values('importance', ascending=False).head(top_n)
            
            # Plot / 绘图
            plt.figure(figsize=figsize)
            sns.barplot(x='importance', y='feature', data=feature_df, palette='viridis')
            plt.title(f'Top {top_n} Feature Importance / 前{top_n}个最重要的特征', 
                     fontsize=14, fontweight='bold')
            plt.xlabel('Importance Score / 重要性分数', fontsize=12)
            plt.ylabel('Feature Name / 特征名称', fontsize=12)
            plt.tight_layout()
            plt.show()
        else:
            print("Model does not have feature_importances_ attribute / 模型没有 feature_importances_ 属性")
    
    @staticmethod
    def plot_backtest_results(df, figsize=(12, 8)):
        """
        绘制回测结果图 / Plot backtest results
        
        Parameters:
        -----------
        df : DataFrame
            Data with cumulative returns columns
            包含累计收益列的数据
        figsize : tuple
            Figure size / 图表尺寸
        """
        fig, axes = plt.subplots(2, 1, figsize=figsize)
        
        # Plot cumulative returns / 绘制累计收益
        axes[0].plot(df['cum_market_returns'], label='Market Returns (Buy & Hold) / 市场收益', 
                    linewidth=2, color='blue')
        axes[0].plot(df['cum_strategy_returns'], label='Strategy Returns (ML) / 策略收益', 
                    linewidth=2, color='red')
        axes[0].set_title('Cumulative Returns / 累计收益', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Cumulative Return', fontsize=10)
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
        
        # Plot price with buy/sell signals / 绘制带买卖信号的价格图
        if 'prediction' in df.columns:
            axes[1].plot(df['close'], label='Price / 价格', linewidth=1.5, color='black', alpha=0.7)
            
            # Mark buy signals (prediction = 1) / 标记买入信号
            buy_signals = df[df['prediction'] == 1]
            axes[1].scatter(buy_signals.index, buy_signals['close'], 
                          color='green', marker='^', s=50, label='Buy Signal / 买入信号', alpha=0.7)
            
            # Mark sell signals (prediction = 0) / 标记卖出信号
            sell_signals = df[df['prediction'] == 0]
            axes[1].scatter(sell_signals.index, sell_signals['close'], 
                          color='red', marker='v', s=50, label='Sell Signal / 卖出信号', alpha=0.7)
            
            axes[1].set_title('Price with Trading Signals / 带交易信号的价格', fontsize=12, fontweight='bold')
            axes[1].set_xlabel('Time / 时间', fontsize=10)
            axes[1].set_ylabel('Price (USDT)', fontsize=10)
            axes[1].legend(loc='best')
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_volume_analysis(df, figsize=(12, 6)):
        """
        绘制成交量分析图 / Plot volume analysis
        
        Parameters:
        -----------
        df : DataFrame
            Data with volume column
            包含成交量列的数据
        figsize : tuple
            Figure size / 图表尺寸
        """
        fig, axes = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [2, 1]})
        
        # Plot price / 绘制价格
        axes[0].plot(df['timestamp'], df['close'], label='Close Price / 收盘价', 
                    linewidth=1.5, color='blue')
        axes[0].set_title('Price and Volume Analysis / 价格和成交量分析', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Price (USDT)', fontsize=10)
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
        
        # Plot volume / 绘制成交量
        axes[1].bar(df['timestamp'], df['volume'], label='Volume / 成交量', 
                   color='orange', alpha=0.6, width=0.8)
        axes[1].set_xlabel('Time / 时间', fontsize=10)
        axes[1].set_ylabel('Volume', fontsize=10)
        axes[1].legend(loc='best')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_correlation_matrix(df, figsize=(10, 8)):
        """
        绘制特征相关性矩阵图 / Plot feature correlation matrix
        
        Parameters:
        -----------
        df : DataFrame
            Data with numeric columns
            包含数值列的数据
        figsize : tuple
            Figure size / 图表尺寸
        """
        # Select only numeric columns / 只选择数值列
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix / 计算相关性矩阵
        corr_matrix = numeric_df.corr()
        
        # Plot heatmap / 绘制热图
        plt.figure(figsize=figsize)
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={"shrink": 0.8})
        plt.title('Feature Correlation Matrix / 特征相关性矩阵', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
