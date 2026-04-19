```python
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
```
