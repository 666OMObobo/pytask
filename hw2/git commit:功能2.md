```python
def random_call(self, count):
        # 判断人数是否合法：1 <= 人数 <= 总人数
        if 1 <= count <= len(self.students):
            return random.sample(self.students, count)  # 随机选count个学生
        return None  # 不合法返回空
```
