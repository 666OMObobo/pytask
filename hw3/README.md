<details>
<summary></summary>
  
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import os

#任务1  数据预处理
#读取数据
folder=os.path.dirname(os.path.abspath(__file__))
csv_path=os.path.join(folder,"ICData.csv")
data=pd.read_csv(csv_path)
print(data.head(5)) 
print(data.shape)
print(data.dtypes)
#新增hour列
data["交易时间"]=pd.to_datetime(data["交易时间"])
data["hour"]=data["交易时间"].dt.hour
#print(data["hour"])#（调试）
#新增ride_stops 列
data["ride_stops"]=abs(data["下车站点"]-data["上车站点"])
delete_num=len(data)-len(data[data["ride_stops"]!=0])
data=data[data["ride_stops"]!=0]
print(delete_num)
#print(data["ride_stops"])#(调试)
#打印各列缺失值数量
print(len(data[data["线路号"]==0]))
print(len(data[data["车辆编号"]==0]))
print(len(data[data["驾驶员编号"]==0]))
#删除异常行
data=data[(data["线路号"]!=0) & (data["车辆编号"]!=0) & (data["驾驶员编号"]!=0)]
#print(data)

#任务2  时间分布分析
card_np=data["刷卡类型"].to_numpy()
all=np.sum(card_np==0)
hour_np=data["hour"].to_numpy()
morning=np.sum((hour_np<7) & (card_np==0))
night=np.sum((hour_np>=22) & (card_np==0))
print(morning)
print(night)
morning_pct=morning / all
night_pct=night / all
#绘制柱状图
hour_count=data.groupby("hour").size()
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
colors=["red" if hour<7 else "blue" if hour>=22 else "green" for hour in hour_count.index]
plt.bar(x=hour_count.index,height=hour_count.values,color=colors)
plt.title("24小时刷卡量分布柱状图")
plt.xlabel("小时")
plt.ylabel("刷卡量")
plt.xticks(np.arange(0, 24, 2))
plt.grid(axis='y', linestyle='--', alpha=0.7)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='red', label='早间(<7点)'),
    Patch(facecolor='green', label='白天(7-22点)'),
    Patch(facecolor='blue', label='夜间(≥22点)')
]
plt.legend(handles=legend_elements, loc="upper right", fontsize=11)
plt.tight_layout()
save_path=os.path.join(folder,"hour_distribution.png")
plt.savefig(save_path,dpi=150)
plt.show()

#任务3  线路站点分析
def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """
    计算各线路乘客的平均搭乘站点数及其标准差。
    Parameters
    ----------
    df : pd.DataFrame  预处理后的数据集
    route_col : str    线路号列名
    stops_col : str    搭乘站点数列名
    Returns
    -------
    pd.DataFrame  包含列：线路号、mean_stops、std_stops，按 mean_stops 降序排列
    """
    result = df.groupby(route_col)[stops_col].agg(['mean', 'std']).reset_index()
    result.columns = [route_col, 'mean_stops', 'std_stops']
    result = result.sort_values('mean_stops', ascending=False)
    return result

# 1. 调用函数并打印前10行
route_df = analyze_route_stops(data)
print("各线路平均搭乘站点数（前10行）：")
print(route_df.head(10))

# 2. 绘制seaborn水平条形图（均值前15条线路）
top15 = route_df.head(15)
plt.figure(figsize=(12,8))

# 绘制水平条形图
sb.barplot(y=top15['线路号'].astype(str), 
           x=top15['mean_stops'], 
           palette='Blues_d', 
           orient='h')

plt.errorbar(x=top15['mean_stops'], 
             y=range(len(top15)), 
             xerr=top15['std_stops'], 
             fmt='none', 
             c='black', 
             capsize=0.3)

plt.title('各线路平均搭乘站点数 Top15', fontsize=16)
plt.xlabel('平均搭乘站点数', fontsize=12)
plt.ylabel('线路号', fontsize=12)
plt.xlim(0)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
route_save_path = os.path.join(folder, "route_stops.png")
plt.savefig(route_save_path, dpi=150)
plt.show()

#任务4
data['minute'] = data['交易时间'].dt.minute
data['5min'] = (data['minute'] // 5) * 5
data['15min'] = (data['minute'] // 15) * 15

# 1. 找高峰小时
peak_hour = hour_count.idxmax()
peak_count = hour_count.max()
print(f"高峰小时：{peak_hour:02d}:00 ~ {peak_hour+1:02d}:00，刷卡量：{peak_count} 次")

# 筛选该小时数据
peak_df = data[data['hour'] == peak_hour]

# 2. 5分钟统计
max5 = peak_df.groupby('5min').size().max()
max5_time = peak_df.groupby('5min').size().idxmax()
phf5 = peak_count / (12 * max5)
print(f"最大5分钟刷卡量（{peak_hour:02d}:{max5_time:02d}~{peak_hour:02d}:{max5_time+5:02d}）：{max5} 次")
print(f"PHF5 = {peak_count} / (12 × {max5}) = {phf5:.4f}")

# 3. 15分钟统计
max15 = peak_df.groupby('15min').size().max()
max15_time = peak_df.groupby('15min').size().idxmax()
phf15 = peak_count / (4 * max15)
print(f"最大15分钟刷卡量（{peak_hour:02d}:{max15_time:02d}~{peak_hour:02d}:{max15_time+15:02d}）：{max15} 次")
print(f"PHF15 = {peak_count} / (4 × {max15}) = {phf15:.4f}\n")

#任务5
output_folder = os.path.join(folder, "线路驾驶员信息")
os.makedirs(output_folder, exist_ok=True)

routes = range(1101, 1121)
for route in routes:
    sub = data[data['线路号'] == route][['车辆编号', '驾驶员编号']].drop_duplicates()
    path = os.path.join(output_folder, f"{route}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"线路号: {route}\n")
        f.write("车辆编号\t驾驶员编号\n")
        for _, row in sub.iterrows():
            f.write(f"{row['车辆编号']}\t\t{row['驾驶员编号']}\n")
    print(f"已生成：{path}")

print("\n===== 20个文件全部导出成功 =====\n")

#任务6 
top_driver = data.groupby('驾驶员编号').size().sort_values(ascending=False).head(10).values
top_route = data.groupby('线路号').size().sort_values(ascending=False).head(10).values
top_stop = data.groupby('上车站点').size().sort_values(ascending=False).head(10).values
top_car = data.groupby('车辆编号').size().sort_values(ascending=False).head(10).values

# 输出排名
print("===== 服务人次 Top10 司机 =====")
print(data.groupby('驾驶员编号').size().sort_values(ascending=False).head(10))
print("\n===== 服务人次 Top10 线路 =====")
print(data.groupby('线路号').size().sort_values(ascending=False).head(10))
print("\n===== 服务人次 Top10 上车站点 =====")
print(data.groupby('上车站点').size().sort_values(ascending=False).head(10))
print("\n===== 服务人次 Top10 车辆 =====")
print(data.groupby('车辆编号').size().sort_values(ascending=False).head(10))

# 构造热力图矩阵
matrix = np.array([top_driver, top_route, top_stop, top_car])
rows = ['司机', '线路', '上车站点', '车辆']
cols = [f'Top{i+1}' for i in range(10)]

plt.figure(figsize=(14, 6))
sb.heatmap(matrix, annot=True, fmt='d', cmap='YlOrRd', xticklabels=cols, yticklabels=rows)
plt.title('公交服务绩效热力图', fontsize=14)
plt.xlabel('排名')
plt.ylabel('维度')
plt.tight_layout()
plt.savefig(os.path.join(folder, "performance_heatmap.png"), dpi=150, bbox_inches='tight')
plt.show()

# 结论（≥50字）
print("""
结论：从热力图可见，线路的服务人次显著高于司机、站点和车辆，说明客流量高度集中在少数热门线路。
部分司机服务人次远超同行，属于核心骨干司机；部分上车站点为区域枢纽，客流压力大。
整体服务呈现明显的头部集中效应，运营资源可向高分线路与站点倾斜。
""")
```
</details>

# 黄浩楠-25361026-第三次人工智能编程作业

## 1. 任务拆解与 AI 协作策略
步骤1：调用模块部分，大致框架，确定任务
步骤2：任务1,2,3,4,5,6分区，确定处理哪些数据，得到哪些数据，在哪些任务得到/使用
步骤3：利用ai,调用我需要的函数
步骤4：利用课件，ai把代码组合起来

## 2. 核心 Prompt 迭代记录
（展示一次你修改 Prompt 让 AI 代码从'不符合要求'变成'符合规范'的迭代过程）
初代 Prompt：...
AI 生成的问题：...（例如：用了 seaborn 替代 matplotlib 画柱状图 / 函数签名不符合要求 / PHF 计算方法错误）
优化后的 Prompt：...

## 3. Debug 记录
（记录一次解决报错的过程，例如：时区解析报错 / 热力图中文乱码 / ride_stops=0 导致的结果偏差）
报错现象：...
解决过程：...

## 4. 人工代码审查（逐行中文注释）
（贴出任务4 PHF 计算的核心代码，并加上你自己的逐行中文注释）
```python
# 贴入代码及注释
```
