```python
def generate_tickets(self):
        if not self.students:  # 无学生则退出
            print("无学生数据")
            return
        
        shuffled = random.sample(self.students, len(self.students))  # 随机打乱
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_dir, "准考证")   # 准考证文件夹名字
        
        # 如果文件夹不存在，创建文件夹
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        # 遍历学生，每人一个准考证文件
        for idx, stu in enumerate(shuffled, 1):
            filename = os.path.join(folder, f"{idx}.txt")  # 文件路径：准考证/1.txt
            # 写入内容
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"座位号：{idx}\n")
                f.write(f"姓名：{stu.name}\n")
                f.write(f"学号：{stu.student_id}\n")
        
        print("✅ 准考证已全部生成")
```
