```python
def generate_exam_table(self):
        if not self.students:  # 没有学生就无法生成
            print("无学生数据")
            return
        
        shuffled = random.sample(self.students, len(self.students))  # 随机打乱所有学生
        base_dir = os.path.dirname(os.path.abspath(__file__))
        exam_file = os.path.join(base_dir, "考场安排表.txt")
    
        with open(exam_file, "w", encoding="utf-8") as f:
            f.write(f"生成时间：{self.get_time()}\n")  # 写入生成时间
            f.write("="*30 + "\n")  # 分割线
            # 遍历学生，分配座位号
            for idx, stu in enumerate(shuffled, 1):
                f.write(f"座位号：{idx:02d} | 姓名：{stu.name} | 学号：{stu.student_id}\n")
        
        print(f"✅ 考场安排表已生成：{exam_file}")
```
