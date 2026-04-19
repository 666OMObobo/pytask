```python
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
```

## 思路
获取py文件夹的路径,组合得到csv的路径，利用pandas直接获取数据，再完成任务要求，缺失数据直接删除防止干扰统计。














