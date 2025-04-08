import sys
import pandas as pd
from datetime import datetime
import glob
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def process_wechat_statement(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 确保所有列都存在
    required_columns = ['交易时间', '收/支/其他', '金额(元)']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f'缺少必要的列：{col}')
    
    # 将交易时间列转换为datetime类型
    df['交易时间'] = pd.to_datetime(df['交易时间'], errors='coerce')
    # 删除无效的日期
    df = df.dropna(subset=['交易时间'])
    
    # 添加月份列
    df['月份'] = df['交易时间'].dt.strftime('%Y-%m')
    
    # 将金额(元)列转换为数值类型
    df['金额(元)'] = pd.to_numeric(df['金额(元)'], errors='coerce')
    # 删除无效的金额
    df = df.dropna(subset=['金额(元)'])
    
    # 确保收支列的值只包含'收入'和'支出'
    df = df[df['收/支/其他'].isin(['收入', '支出'])]
    
    # 按收/支/其他类型和月份分组统计
    monthly_stats = []
    for month in sorted(df['月份'].unique()):
        month_data = df[df['月份'] == month]
        
        # 计算收入（交易类型为"收入