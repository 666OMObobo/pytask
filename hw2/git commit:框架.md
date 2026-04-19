## 所需模块
<details>
<summary>模块</summary>

```python  
import os  
import random  
from datetime import datetime 
```
</details>

## 读取/储存/使用数据
<details>
<summary></summary>

```python
#学生数据  
class Student:
    # 构造方法：创建学生对象时，自动给学生赋值
    def __init__(self, name, gender, cls, student_id, college):
        self.name = name          # 学生姓名
        self.gender = gender      # 学生性别
        self.cls = cls            # 学生班级
        self.student_id = student_id  # 学生学号
        self.college = college    # 学生学院

    # 打印学生格式
    def __str__(self):
        return f"姓名：{self.name} | 性别：{self.gender} | 班级：{self.cls} | 学号：{self.student_id} | 学院：{self.college}"

#考试系统数据
class ExamSystem:
    # 系统初始化：创建系统时自动运行
    def __init__(self, filename):
        self.filename = filename      # 保存学生文件的名字
        self.students = []            # 空列表：存放所有学生对象
        self.student_dict = {}        # 空字典：用学号快速查学生（速度更快）
        self.load_students()          # 自动调用方法：加载学生文件

    # 静态方法：获取当前时间（不需要创建对象就能用）
    @staticmethod
    def get_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间：年-月-日 时:分:秒

    def load_students(self):
        try:  # try：尝试执行代码，出错不崩溃，跳到except
            # 获取当前Python文件所在的文件夹路径（解决找不到文件问题）
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # 拼接：当前文件夹 + 学生文件名 = 完整路径
            real_file = os.path.join(base_dir, self.filename)

            print("正在读取文件：", real_file)  # 打印正在读取的路径，方便调试

            # 打开文件：只读模式，编码utf-8
            with open(real_file, "r", encoding="utf-8") as f:
                lines = f.readlines()  # 读取文件所有行，存入列表

                # 遍历每一行：从第2行开始
                for line in lines[1:]:
                    line = line.strip()        # 去掉空格、换行符
                    if not line:              # 如果是空行，跳过
                        continue
                    parts = line.split("\t")  # 按制表符\t切分数据（表格文件格式）
                    
                    # 检查：一行必须是6个数据（序号、姓名、性别、班级、学号、学院）
                    if len(parts) != 6:
                        print(f"跳过错误行：{line}")
                        continue
                    
                    # 解包：把切分后的6个数据分别赋值
                    _, name, gender, cls, sid, college = parts
                    # 创建学生对象
                    stu = Student(name, gender, cls, sid, college)
                    self.students.append(stu)        # 加入学生列表
                    self.student_dict[sid] = stu     # 加入字典（学号为键）

            # 读取完成，提示成功
            print(f"✅ 加载成功，共 {len(self.students)} 名学生")

        # 异常1：文件找不到
        except FileNotFoundError:
            print("\n❌ 没找到文件！")
        # 异常2：其他错误
        except Exception as e:
            print(f"错误：{e}")

```
</details>
 
## 主程序(操作界面)
<details>
<summary>界面</summary>

```python  
print("\n===== 学生信息与考场管理系统 =====")
print("1. 按学号查询学生信息")
print("2. 随机点名")
print("3. 生成考场安排表")
print("4. 生成准考证文件")
print("0. 退出")
choice = input("请输入功能编号：")
if choice == "1":
elif choice == "2":
elif choice == "3":
elif choice == "4":
elif choice == "0":
else:
print("无效选项")     
```
</details>

## 功能
<details>
<summary>功能菜单</summary>
<details>
<summary>功能1</summary>
  
```python
def search_by_id(self, student_id):
```
</details>

<details>
<summary>功能2</summary>

```python
def random_call(self, count):
```
</details>

<details>
<summary>功能3</summary>

```python
def generate_exam_table(self):
```
</details>

<details>
<summary>功能4</summary>

```python
def generate_tickets(self):
```
</details>
</details>

















