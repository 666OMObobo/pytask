```python
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
```
