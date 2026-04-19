```python
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


```
