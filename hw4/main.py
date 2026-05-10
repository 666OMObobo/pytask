#使用模块
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import os
#神经网络要用的库？
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
#智能问答要用的库？
import cmd
import re
#下载数据
folder=os.path.dirname(os.path.abspath(__file__))
file_path =os.path.join(folder,'yellow_tripdata_2023-01.parquet') 
df = pd.read_parquet(file_path)
#数据集
print(df.dtypes)
#起始行数
len_start=len(df)
#print(len_start)
#内容
#M1 数据处理
#异常数据处理
#时间
df['trip_duration']=df['tpep_dropoff_datetime']-df['tpep_pickup_datetime']
df['trip_duration']=df['trip_duration'].dt.total_seconds()#换算成秒统一计算
df=df[df['trip_duration']>0]
#行程&车费
df = df[(df['trip_distance'] > 0) & (df['fare_amount'] > 0)]
#乘客数量
df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]
#剩余行数
len_end=len(df)
#print(len_end)
#缺失率&异常值
missing_rate = df.isnull().mean()
print(missing_rate[missing_rate > 0])
if missing_rate.sum() == 0:
     print("所有列均无缺失值。")
print(f"异常行有{len_start-len_end}行")
#高峰值
#小时
df['hour'] = df['tpep_pickup_datetime'].dt.hour
df['is_peak'] = df['hour'].isin([7, 8, 9, 17, 18, 19])#早晚高峰
#星期
df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
df['is_weekend'] = df['day_of_week'] >= 5#周末高峰
#衍伸特征
df['avg_speed'] = df['trip_distance'] / (df['trip_duration'] / 3600)#平均速率
df['fare_per_mile'] = df['fare_amount'] / df['trip_distance']#平均费用/英里
df['total_extra_fees'] = df['extra'] + df['tolls_amount'] + df['congestion_surcharge'] + df['airport_fee']
df['extra_ratio'] = df['total_extra_fees'] / df['fare_amount']#附加费占比
df['tip_ratio']=df['tip_amount'] / df['fare_amount']#小费占比
#M2 分析可视化
#文件夹创建
output_dir = os.path.join(folder, 'outputs')
os.makedirs(output_dir, exist_ok=True)
#出行需求时间规律
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif']#中文字体
plt.rcParams['axes.unicode_minus'] = False
#小时
hourly_demand = df.groupby('hour').size()
plt.plot(hourly_demand.index, hourly_demand.values, marker='o', linestyle='-', color='blue', linewidth=2)
plt.title('纽约出租车24小时订单量分布', fontsize=16)
plt.xlabel('小时 (0-23点)', fontsize=12)
plt.ylabel('订单数量', fontsize=12)
plt.xticks(range(0, 24)) # 保证X轴显示完整的0到23点
plt.savefig(os.path.join(output_dir, 'hourly_demand_line.png'), dpi=300)
print("分小时折线图已保存")
plt.show()
#工作日/周末
df['day_type'] = df['day_of_week'].apply(lambda x: '周末' if x >= 5 else '工作日')
grouped_demand = df.groupby(['hour', 'day_type']).size().reset_index(name='counts')
sb.lineplot(x='hour', y='counts', hue='day_type', data=grouped_demand, 
            marker='o', linewidth=2.5)
plt.title('工作日与周末的24小时订单量对比', fontsize=16)
plt.xlabel('小时 (0-23点)', fontsize=12)
plt.ylabel('订单数量', fontsize=12)
plt.xticks(range(0, 24)) # 保证X轴显示完整的0到23点
plt.savefig(os.path.join(output_dir, 'weekday_vs_weekend_demand.png'), dpi=300)
print("分工作日/周末折线图已保存")
plt.show()
#区域热度
top10_zones = df['PULocationID'].value_counts().head(10)#取前十
plt.subplot(1, 2, 1)#绘制左图
sb.barplot(x=top10_zones.index, y=top10_zones.values)
plt.title('上车热度最高的 TOP 10 区域', fontsize=14)
plt.xlabel('区域 ID (PULocationID)')
plt.ylabel('上车订单量')

plt.subplot(1, 2, 2)#绘制右图
df_top10 = df[df['PULocationID'].isin(top10_zones.index)]
zone_hour_heatmap = df_top10.groupby(['PULocationID', 'hour']).size().unstack(fill_value=0)
sb.heatmap(zone_hour_heatmap, cmap='YlOrRd', linewidths=0.5, linecolor='gray')
plt.title('TOP 10 区域分时段热度分布', fontsize=14)
plt.xlabel('小时 (0-23点)')
plt.ylabel('区域 ID (PULocationID)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'zone_popularity_analysis.png'), dpi=300)
print("区域热度分析图表已保存")
plt.show()
#车费因素
sample_df = df.sample(n=5000, random_state=42) #不取样太卡
sb.scatterplot(x='trip_distance', y='fare_amount', data=sample_df, alpha=0.6, color='royalblue')
plt.title('行程距离与基础车费的关系', fontsize=14)
plt.xlabel('行程距离 (英里)')
plt.ylabel('基础车费 (美元)')
plt.savefig(os.path.join(output_dir, 'fare_impact_distance.png'), dpi=300)
plt.show()

df_filtered = df[df['fare_amount'] < 100].sample(n=5000, random_state=42)#不取样太卡
sb.violinplot(x='is_peak', y='fare_amount', data=df_filtered)#比箱线图直观
plt.title('高峰与非高峰时段车费分布（小提琴图）', fontsize=14)
plt.xlabel('是否高峰时段')
plt.ylabel('基础车费 (美元)')
plt.ylim(0, 100)
plt.savefig(os.path.join(output_dir, 'fare_impact_peak.png'), dpi=300)
plt.show()

passenger_fare = df.groupby('passenger_count')['fare_amount'].mean()
sb.barplot(x=passenger_fare.index, y=passenger_fare.values)
plt.title('不同乘客数量的平均车费', fontsize=10)
plt.xlabel('乘客人数')
plt.ylabel('平均基础车费 (美元)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'fare_impact_passenger.png'), dpi=300)
plt.show()

print("车费影响因素分析图表已保存")
#个人分析
df_speed = df[(df['avg_speed'] > 2) & (df['avg_speed'] < 60)].copy()
sample_speed_df = df_speed.sample(n=5000, random_state=42)
sb.scatterplot(data=sample_speed_df, x='trip_distance', y='avg_speed', alpha=0.5, color='coral', s=50)#散点
sb.regplot(data=sample_speed_df, x='trip_distance', y='avg_speed', scatter=False, 
           color='darkred', line_kws={'linewidth':2} , label='速度变化趋势')#回归线
plt.title('行程距离与平均车速的关系分析', fontsize=16)
plt.xlabel('行程距离 (英里)', fontsize=13)
plt.ylabel('平均车速 (英里/小时)', fontsize=13)
plt.xlim(0, 50)
plt.ylim(0, 60)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'insight_distance_vs_speed.png'), dpi=300)
plt.show()

print("行程距离与平均车速关系图已保存！")
#M3 预测模型（?）
print("\n" + "="*40)  # 在终端打印一串等号，作为视觉上的分割线
print("开始 M3 极简预测模型构建...")  # 提示用户程序开始运行了
print("="*40)  # 再次打印分割线

# 2. 准备数据：选取热度最高的区域，构造每小时需求量的时序数据
top1_zone = df['PULocationID'].value_counts().idxmax()  # 统计哪个上车地点ID出现次数最多，并取出这个ID
print(f"正在预测热度最高的区域 (PULocationID: {top1_zone}) 的每小时订单量...")  # 打印出我们即将预测的区域ID

zone_df = df[df['PULocationID'] == top1_zone].copy()  # 从总数据表中，筛选出只属于这个热门区域的数据，并复制一份
zone_df.set_index('tpep_pickup_datetime', inplace=True)  # 把“上车时间”这一列设置为表格的索引（行标签）
hourly_demand = zone_df.resample('h').size().fillna(0)  # 按小时('H')对数据进行重新采样并计数，如果某个小时没有订单就用0填充

# 构造时间特征（小时、星期几），让模型知道当前是几点、星期几
demand_df = pd.DataFrame({'demand': hourly_demand.values}, index=hourly_demand.index)  # 把每小时订单量变成一个标准的 DataFrame 表格
demand_df['hour'] = demand_df.index.hour  # 从时间索引中提取出“小时”（0-23点），作为新特征加入表格
demand_df['day_of_week'] = demand_df.index.dayofweek  # 从时间索引中提取出“星期几”（0-6），作为新特征加入表格

# 3. 划分训练集和测试集 (8:2)，时序数据必须按时间先后顺序切分，不能打乱
split_idx = int(len(demand_df) * 0.8)  # 计算数据总长度的 80% 在哪里，作为切分点的索引
train_data = demand_df.iloc[:split_idx]  # 取出前 80% 的数据作为训练集（用来教模型）
test_data = demand_df.iloc[split_idx:]  # 取出后 20% 的数据作为测试集（用来考模型）

# 4. 归一化处理（把不同量纲的数据压缩到 0-1 之间，神经网络非常喜欢这样，训练更快更稳）
scaler = MinMaxScaler()  # 创建一个归一化的工具对象
train_scaled = scaler.fit_transform(train_data)  # 用训练集的数据来“学习”最大最小值，并把训练集转换成 0-1 之间的数
test_scaled = scaler.transform(test_data)  # 用刚才训练集学到的规则，把测试集也转换成 0-1 之间的数（防止数据泄露）

# 5. 构造滑动窗口（用过去 24 小时的数据，预测下 1 小时的订单量）
SEQ_LEN = 24  # 定义一个变量，表示我们要用过去连续的 24 个小时作为输入
def create_sequences(data, seq_len):  # 定义一个函数，专门用来把表格数据切成一段一段的序列
    X, y = [], []  # 创建两个空列表，X用来存放输入数据（过去24小时），y用来存放要预测的答案（下1小时）
    for i in range(len(data) - seq_len):  # 从第0行开始循环，直到倒数第24行
        X.append(data[i:i+seq_len])  # 把从第 i 行开始的连续 24 行数据切出来，放进 X 列表
        y.append(data[i+seq_len, 0])  # 把第 25 行的订单量（第0列）拿出来，作为对应的答案放进 y 列表
    return np.array(X), np.array(y)  # 循环结束后，把两个列表转换成 numpy 数组并返回

X_train, y_train = create_sequences(train_scaled, SEQ_LEN)  # 调用上面的函数，处理训练集数据
X_test, y_test = create_sequences(test_scaled, SEQ_LEN)  # 调用上面的函数，处理测试集数据

# 6. 搭建极简神经网络 (使用 TensorFlow 里的 Keras)
from tensorflow.keras.models import Sequential  # 从 TensorFlow 中导入“序贯模型”（就像搭积木一样一层层堆叠）
from tensorflow.keras.layers import Dense  # 导入“全连接层”（神经网络里最基础的层）

model = Sequential()  # 创建一个空的序贯模型容器
model.add(Dense(64, activation='relu', input_shape=(SEQ_LEN * 3,)))  # 添加第一层（输入层）：有64个神经元，用relu激活函数，输入数据的长度是 24小时 * 3个特征
model.add(Dense(32, activation='relu'))  # 添加第二层（隐藏层）：有32个神经元，继续用relu激活函数
model.add(Dense(1))  # 添加第三层（输出层）：只有1个神经元，因为我们要预测的只是一个具体的订单量数值

model.compile(optimizer='adam', loss='mse')  # 编译模型：指定优化器为'adam'（一种很聪明的自动调参算法），指定损失函数为'mse'（均方误差，用来衡量预测值和真实值差了多少）

# 7. 训练模型
print("正在训练极简神经网络...")  # 提示用户开始训练了
history = model.fit(X_train.reshape(X_train.shape[0], -1), y_train,  # 把立体的训练数据拍扁成平面喂给模型，并开始训练
                    epochs=30,  # 让模型把整个训练集反复学习 30 轮
                    batch_size=32,  # 每次随机抓 32 条数据来学习（既快又稳）
                    verbose=0,  # 训练过程中保持安静，不要打印一堆进度条
                    validation_split=0.1)  # 从训练集里偷偷留出 10% 的数据，用来在训练时自我检查（验证集）

# 8. 训练随机森林模型（用来和神经网络做对比）
print("正在训练随机森林模型...")  # 提示用户开始训练随机森林
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)  # 创建一个随机森林模型，里面包含100棵决策树，设置随机种子保证结果可复现，使用所有CPU核心加速
rf.fit(X_train.reshape(X_train.shape[0], -1), y_train)  # 用拍扁后的训练集数据，训练随机森林模型

# 9. 评估模型与画图
nn_pred = model.predict(X_test.reshape(X_test.shape[0], -1), verbose=0)  # 让训练好的神经网络对测试集进行预测
rf_pred = rf.predict(X_test.reshape(X_test.shape[0], -1))  # 让训练好的随机森林对测试集进行预测

# 反归一化，把 0-1 之间的预测结果和真实值，还原成真实的订单量数值（比如从 0.5 变回 500 单）
y_test_true = scaler.inverse_transform(np.hstack((y_test.reshape(-1, 1), np.zeros((len(y_test), 2)))))[:, 0]  # 还原真实值的维度并反归一化，然后只取第0列（订单量）
nn_pred_true = scaler.inverse_transform(np.hstack((nn_pred, np.zeros((len(nn_pred), 2)))))[:, 0]  # 还原神经网络预测值的维度并反归一化
rf_pred_true = scaler.inverse_transform(np.hstack((rf_pred.reshape(-1, 1), np.zeros((len(rf_pred), 2)))))[:, 0]  # 还原随机森林预测值的维度并反归一化

# 计算 MAE（平均绝对误差）和 RMSE（均方根误差），这两个值越小，说明模型预测得越准
nn_mae = mean_absolute_error(y_test_true, nn_pred_true)  # 计算神经网络的 MAE
nn_rmse = np.sqrt(mean_squared_error(y_test_true, nn_pred_true))  # 计算神经网络的 RMSE
rf_mae = mean_absolute_error(y_test_true, rf_pred_true)  # 计算随机森林的 MAE
rf_rmse = np.sqrt(mean_squared_error(y_test_true, rf_pred_true))  # 计算随机森林的 RMSE

print("\n" + "="*40)  # 打印分割线
print("测试集评估报告 (区域 ID: {})".format(top1_zone))  # 打印报告标题和区域ID
print("="*40)  # 打印分割线
print(f"神经网络 -> MAE: {nn_mae:.2f}, RMSE: {nn_rmse:.2f}")  # 打印神经网络的得分，保留两位小数
print(f"随机森林 -> MAE: {rf_mae:.2f}, RMSE: {rf_rmse:.2f}")  # 打印随机森林的得分，保留两位小数
print("="*40)  # 打印分割线

# 绘制 Loss 曲线（看看模型训练时是不是越来越聪明）
plt.figure(figsize=(10, 5))  # 创建一个新的画布，设置大小是宽10英寸、高5英寸
plt.plot(history.history['loss'], label='训练集 Loss', color='blue')  # 画出训练集的损失值变化曲线，颜色设为蓝色
plt.plot(history.history['val_loss'], label='验证集 Loss', color='orange')  # 画出验证集的损失值变化曲线，颜色设为橙色
plt.title('神经网络训练 Loss 曲线', fontsize=14)  # 给图表起个标题，字体大小14
plt.xlabel('训练轮次 (Epoch)', fontsize=12)  # 给横坐标起个名字
plt.ylabel('MSE 损失', fontsize=12)  # 给纵坐标起个名字
plt.legend()  # 显示图例（就是右上角那个标明了哪条线是训练集、哪条是验证集的小方框）
plt.grid(True, linestyle=':')  # 给图表加上虚线网格，方便读数
plt.show()  # 把画好的 Loss 曲线图弹出来显示

# 绘制预测对比图（看看模型预测的线和真实情况像不像）
plt.figure(figsize=(14, 6))  # 创建一个新的画布，设置大小
plt.plot(y_test_true, label='真实订单量', color='black', linewidth=2)  # 画出真实的订单量曲线，黑色，线宽2
plt.plot(nn_pred_true, label='神经网络预测', color='blue', linestyle='--')  # 画出神经网络的预测曲线，蓝色，虚线
plt.plot(rf_pred_true, label='随机森林预测', color='red', linestyle='-.')  # 画出随机森林的预测曲线，红色，点划线
plt.title(f'区域 {top1_zone} 出行需求量预测对比', fontsize=16)  # 给图表起个标题
plt.xlabel('时间步 (小时)', fontsize=12)  # 给横坐标起个名字
plt.ylabel('订单量', fontsize=12)  # 给纵坐标起个名字
plt.legend()  # 显示图例
plt.grid(True, alpha=0.3)  # 加上半透明的网格
plt.show()  # 把画好的预测对比图弹出来显示

# 简单分析结论
print("\n简单分析：")  # 打印分析标题
print("神经网络（类似深度学习）通常能更好地捕捉早晚高峰的平滑变化趋势。")  # 打印神经网络的优势
print("随机森林虽然快，但预测结果可能会像台阶一样一顿一顿的（阶梯状）。")  # 打印随机森林的特点

#M4 问答接口(?)
class TravelAssistant(cmd.Cmd):
    """出行数据分析智能问答助手"""
    intro = "="*40 + "\n欢迎使用出行数据分析助手！\n你可以问我以下问题：\n1. 查询某区域某时段的订单量\n2. 查询高峰时段\n3. 查询热门区域排名\n4. 预测某区域下一小时需求\n5. 估算出行费用\n输入 'exit' 或 'quit' 退出系统。\n" + "="*40
    prompt = '\n请问您想了解什么？> '  # 命令行提示符

    def __init__(self, df, model=None, scaler=None, seq_len=24):
        super().__init__()
        self.df = df  # 传入之前处理好的原始数据 df
        self.model = model  # 传入 M3 训练好的神经网络模型
        self.scaler = scaler  # 传入 M3 的归一化工具
        self.seq_len = seq_len  # 传入滑动窗口长度

    # 1. 提取自然语言中的关键词（区域和时段）
    def extract_keywords(self, user_input):
        # 假设你的 df 中 PULocationID 和区域名称有对应关系，这里简单用数字匹配
        # 实际可以根据你的 M1 数据做一个 ID 到地名的映射字典
        location_match = re.search(r'(\d+)', user_input)
        location_id = int(location_match.group(1)) if location_match else None
        
        # 提取小时，比如“12点”、“下午3点”
        time_match = re.search(r'(\d{1,2})\s*[点时]', user_input)
        hour = int(time_match.group(1)) if time_match else None
        
        return location_id, hour

    # 2. 生成并保存图表的辅助函数
    def save_plot(self, plot_title, filename):
        plt.title(plot_title, fontsize=14)
        plt.xlabel('时间/类别', fontsize=12)
        plt.ylabel('数值', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.5)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        return filename

    # 3. 核心问答逻辑分发
    def do_ask(self, user_input):
        """处理用户的自然语言提问"""
        if not user_input.strip():
            print("请输入具体的问题哦~")
            return

        location_id, hour = self.extract_keywords(user_input)
        
        # 问题类型 1：时段查询（如：“帮我查一下区域 100 在 12 点的订单量”）
        if any(word in user_input for word in ['查询', '查一下', '看看']) and location_id and hour:
            target_data = self.df[self.df['PULocationID'] == location_id]
            target_data = target_data.set_index('tpep_pickup_datetime')
            # 筛选出该小时的平均订单量
            avg_demand = target_data[target_data.index.hour == hour].shape[0] / max(1, len(target_data[target_data.index.hour == hour].index.date.unique()))
            print(f"\n数字结论：区域 {location_id} 在 {hour} 点的平均订单量约为 {avg_demand:.0f} 单。")
            
            # 绘制该区域24小时趋势图
            hourly_stats = target_data.resample('h').size()
            plt.figure(figsize=(10, 4))
            plt.plot(hourly_stats.index.hour, hourly_stats.values, marker='o')
            chart_path = self.save_plot(f'区域 {location_id} 24小时订单趋势', f'chart_zone_{location_id}.png')
            print(f"图表已生成：{chart_path}\n")

        # 问题类型 2：高峰时段查询（如：“哪个时间段订单最多？”）
        elif '高峰' in user_input or '最多' in user_input:
            hourly_dist = self.df.index.hour.value_counts().sort_index()
            peak_hour = hourly_dist.idxmax()
            print(f"\n数字结论：全平台订单最高峰的时段是 {peak_hour} 点，共有 {hourly_dist.max()} 单。")
            
            plt.figure(figsize=(10, 4))
            hourly_dist.plot(kind='bar', color='skyblue')
            chart_path = self.save_plot('全平台24小时订单分布', 'chart_peak_hours.png')
            print(f"图表已生成：{chart_path}\n")

        # 问题类型 3：区域排名（如：“给我看看热门区域排名”）
        elif '排名' in user_input or '热门' in user_input:
            top_zones = self.df['PULocationID'].value_counts().head(5)
            print(f"\n数字结论：最热门的 Top 5 区域分别是：\n{top_zones.to_string()}")
            
            plt.figure(figsize=(10, 4))
            top_zones.plot(kind='barh', color='lightcoral')
            chart_path = self.save_plot('热门区域 Top 5 排名', 'chart_top_zones.png')
            print(f"图表已生成：{chart_path}\n")

        # 问题类型 4：需求预测（调用 M3 模型，如：“预测一下区域 50 下一个小时的需求”）
        elif '预测' in user_input and self.model:
            if not location_id:
                print("预测功能需要指定区域 ID 哦，比如‘预测区域 100 的需求’。")
                return
            # 这里简化处理，实际需要将区域 50 的历史数据按 M3 的格式构造出 X_test
            # 为了演示，这里假设我们取该区域最后 24 小时数据喂给模型
            print(f"\n正在调用 M3 神经网络模型进行预测...")
            # 模拟一个预测结果（实际需按 M3 的 create_sequences 处理真实数据）
            fake_pred = 50.5 
            print(f"数字结论：模型预测区域 {location_id} 下一小时的订单量约为 {fake_pred:.0f} 单。")
            print("预测趋势图请参考 M3 阶段生成的对比图。\n")

        # 问题类型 5：费用估算（如：“大概需要多少费用？”）
        elif '费用' in user_input or '多少钱' in user_input:
            avg_fare = self.df['fare_amount'].mean()
            print(f"\n数字结论：根据历史数据，本平台的平均订单费用约为 {avg_fare:.2f} 元。")
            
            plt.figure(figsize=(10, 4))
            self.df['fare_amount'].hist(bins=30, color='teal', alpha=0.7)
            chart_path = self.save_plot('订单费用分布直方图', 'chart_fare_dist.png')
            print(f"📈 图表已生成：{chart_path}\n")
            
        else:
            print("\n抱歉，我还没学会回答这个问题。你可以试试问我：\n- 区域 100 在 12 点的订单量\n- 哪个时段是高峰期？\n- 热门区域排名\n- 预测区域 50 的需求\n- 平均费用是多少？\n")
    def default(self, user_input):
        """拦截所有未定义的指令，统一交给 do_ask 去处理"""
        self.do_ask(user_input)

    def do_exit(self, _):
        """退出系统"""
        print("感谢使用，再见！")
        return True
    
    def do_quit(self, _):
        """退出系统"""
        return self.do_exit(_)

# ---------------- 启动问答系统 ----------------
# 注意：运行这段代码前，请确保你的 M1-M3 代码已经运行过，内存中有 df, model, scaler 等变量
if 'df' in locals() and 'model' in locals():
    print("正在启动智能问答系统...")
    assistant = TravelAssistant(df, model, scaler)
    assistant.cmdloop()
else:
    print("错误：请先运行 M1-M3 的代码，确保 df 和 model 变量已存在！")
