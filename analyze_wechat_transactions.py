import sys
import os
import pandas as pd
import glob
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QFileDialog, QTableWidget, QTableWidgetItem,
                             QLabel, QHBoxLayout, QProgressBar)
import matplotlib.pyplot as plt

# 设置matplotlib中文字体
import platform
if platform.system() == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Windows系统使用微软雅黑字体
else:
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'Apple LiGothic Medium']  # macOS系统使用苹果系统字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

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
        
        # 计算收入和支出
        income = month_data[month_data['收/支/其他'] == '收入']['金额(元)'].sum()
        expense = month_data[month_data['收/支/其他'] == '支出']['金额(元)'].sum()
        
        monthly_stats.append({
            '月份': month,
            '收入': income,
            '支出': expense,
            '净收入': income - expense
        })
    
    return pd.DataFrame(monthly_stats)

class WeChatAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('微信账单分析器')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # 创建顶部按钮和标签区域
        top_layout = QHBoxLayout()
        self.select_dir_btn = QPushButton('选择文件夹', self)
        self.select_dir_btn.clicked.connect(self.select_directory)
        self.status_label = QLabel('请选择包含微信账单Excel文件的文件夹')
        top_layout.addWidget(self.select_dir_btn)
        top_layout.addWidget(self.status_label)
        layout.addLayout(top_layout)
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['月份', '收入(元)', '支出(元)', '净收入(元)'])
        layout.addWidget(self.table)
        
        # 创建图表
        # self.figure = Figure(figsize=(8, 4))
        # self.canvas = FigureCanvas(self.figure)
        # layout.addWidget(self.canvas)
        
        self.final_stats = None
    
    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if dir_path:
            try:
                self.process_directory(dir_path)
            except Exception as e:
                self.status_label.setText(f'处理文件时出错：{str(e)}')
    
    def process_directory(self, dir_path):
        excel_files = glob.glob(f'{dir_path}/*.xlsx')
        if not excel_files:
            self.status_label.setText('所选文件夹中没有找到Excel文件')
            return
        
        # 显示进度条并设置初始值
        self.progress_bar.setVisible(True)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(len(excel_files))
        self.progress_bar.setValue(0)
        
        all_stats = []
        for i, file in enumerate(excel_files, 1):
            try:
                # 更新状态标签显示当前处理的文件
                self.status_label.setText(f'正在处理: {os.path.basename(file)}')
                stats = process_wechat_statement(file)
                all_stats.append(stats)
                # 更新进度条
                self.progress_bar.setValue(i)
                QApplication.processEvents()  # 确保UI更新
            except Exception as e:
                self.status_label.setText(f'处理文件 {file} 时出错: {str(e)}')
                self.progress_bar.setVisible(False)
                return
        
        if all_stats:
            self.final_stats = pd.concat(all_stats).groupby('月份').sum().reset_index()
            self.final_stats = self.final_stats.sort_values('月份')
            self.update_table()
            self.update_chart()
            self.status_label.setText('数据处理完成')
            self.progress_bar.setVisible(False)  # 处理完成后隐藏进度条
    
    def update_table(self):
        if self.final_stats is None:
            return
        
        # 计算合计和平均值
        total_income = self.final_stats['收入'].sum()
        total_expense = self.final_stats['支出'].sum()
        total_net = self.final_stats['净收入'].sum()
        
        avg_income = self.final_stats['收入'].mean()
        avg_expense = self.final_stats['支出'].mean()
        avg_net = self.final_stats['净收入'].mean()
        
        # 设置表格行数（原数据行数 + 2行用于显示合计和平均值）
        self.table.setRowCount(len(self.final_stats) + 2)
        
        # 填充数据行
        for i, row in self.final_stats.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['月份'])))
            self.table.setItem(i, 1, QTableWidgetItem(f'¥{row["收入"]:,.2f}'))
            self.table.setItem(i, 2, QTableWidgetItem(f'¥{row["支出"]:,.2f}'))
            self.table.setItem(i, 3, QTableWidgetItem(f'¥{row["净收入"]:,.2f}'))
        
        # 添加合计行
        total_row = len(self.final_stats)
        self.table.setItem(total_row, 0, QTableWidgetItem('合计'))
        self.table.setItem(total_row, 1, QTableWidgetItem(f'¥{total_income:,.2f}'))
        self.table.setItem(total_row, 2, QTableWidgetItem(f'¥{total_expense:,.2f}'))
        self.table.setItem(total_row, 3, QTableWidgetItem(f'¥{total_net:,.2f}'))
        
        # 添加平均值行
        avg_row = len(self.final_stats) + 1
        self.table.setItem(avg_row, 0, QTableWidgetItem('平均值'))
        self.table.setItem(avg_row, 1, QTableWidgetItem(f'¥{avg_income:,.2f}'))
        self.table.setItem(avg_row, 2, QTableWidgetItem(f'¥{avg_expense:,.2f}'))
        self.table.setItem(avg_row, 3, QTableWidgetItem(f'¥{avg_net:,.2f}'))
        
        self.table.resizeColumnsToContents()
    
    def update_chart(self):
        if self.final_stats is None:
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        months = self.final_stats['月份']
        ax.plot(months, self.final_stats['收入'], label='收入', marker='o')
        ax.plot(months, self.final_stats['支出'], label='支出', marker='o')
        ax.plot(months, self.final_stats['净收入'], label='净收入', marker='o')
        
        # 设置字体属性
        font_properties = {'family': plt.rcParams['font.sans-serif'][0]}
        ax.set_title('月度收支趋势', fontdict=font_properties)
        ax.set_xlabel('月份', fontdict=font_properties)
        ax.set_ylabel('金额(元)', fontdict=font_properties)
        ax.legend(prop=font_properties)
        ax.grid(True)
        
        # 旋转x轴标签以防重叠
        plt.xticks(rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = WeChatAnalyzer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()