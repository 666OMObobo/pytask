```python
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
