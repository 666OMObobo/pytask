<details>
<summary></summary>
  
```python
#所需模块
import os               # 操作系统工具：处理文件、文件夹、路径
import random           # 随机工具：随机点名、随机排座位
from datetime import datetime  # 时间工具：获取当前时间

#学生数据
class Student:
    # 构造方法：创建学生对象时，自动给学生赋值
    def __init__(self, name, gender, cls, student_id, college):
        self.name = name          # 学生姓名
        self.gender = gender      # 学生性别
        self.cls = cls            # 学生班级
        self.student_id = student_id  # 学生学号
        self.college = college    # 学生学院

    # 打印学生时格式
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

    # 读取学生名单文件
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

    # 功能1：按学号查询学生
    def search_by_id(self, student_id):
        return self.student_dict.get(student_id)  # 字典查找：有则返回学生，无则返回None

    # 功能2：随机点名
    def random_call(self, count):
        # 判断人数是否合法：1 <= 人数 <= 总人数
        if 1 <= count <= len(self.students):
            return random.sample(self.students, count)  # 随机选count个学生
        return None  # 不合法返回空

    # 功能3：生成考场安排表
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

    #功能4：批量生成准考证文件
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

#主程序
if __name__ == "__main__":
    # 创建系统对象，自动加载学生文件
    system = ExamSystem("人工智能编程语言学生名单.txt")

    # 无限循环菜单
    while True:
        print("\n===== 学生信息与考场管理系统 =====")
        print("1. 按学号查询学生信息")
        print("2. 随机点名")
        print("3. 生成考场安排表")
        print("4. 生成准考证文件")
        print("0. 退出")
        
        choice = input("请输入功能编号：")  # 获取用户输入

        # 根据用户选择执行功能
        if choice == "1":
            sid = input("请输入学号：")
            stu = system.search_by_id(sid)
            print(stu if stu else "❌ 未找到学生")

        elif choice == "2":
            try:
                n = int(input("输入点名人数："))
                res = system.random_call(n)
                if not res:
                    print(f"请输入1~{len(system.students)}")
                else:
                    print("\n===== 点名结果 =====")
                    for i, s in enumerate(res, 1):
                        print(f"{i}. {s.name} {s.student_id}")
            except:
                print("请输入数字")

        elif choice == "3":
            system.generate_exam_table()

        elif choice == "4":
            system.generate_tickets()

        elif choice == "0":
            print("👋 退出成功")
            break  # 结束循环，程序关闭

        else:
            print("无效选项") 
```
</details>

# 黄浩楠-25361026-第二次人工智能编程作业
## 1. 任务拆解与 AI 协作策略
步骤1:敲定框架，模块区，读取数据区，数据操作区》功能区》具体函数，主界面控制区  
步骤2：首先读取文本数据并储存，方便操作，将学生的数据归为学生类，将其中的数据分别添加到对应的列表(点名)，字典(查学号)  
步骤3：写函数后续在主程序调用，用步骤2的数据分别实现4个功能  
步骤4：编写主界面，用于输入操作指令  
## 2. 核心 Prompt 迭代记录
初代prompt:根据学生的信息，随机生成座位号，并生成对应的.txt文件    
AI问题:生成的文件与py文件不在同一文件夹    
优化后prompt:要求文件与提供的.txt在同一文件夹  
## 3. Debug 与异常处理记录
未找到文件，程序无法找到处在同一文件夹的.txt。AI方案先获取py文件的文件夹路径，再用文件名拼接为完整路径，再次运行，依旧无法读取，发现系统隐藏的文件名后缀.txt未加入，改正后成功运行
## 4. 人工代码审查 (Code Review)
（请贴出一段 AI 生成的核心逻辑代码，并加上你自己的逐行中文注释，证明你完全理解了它的运行机制）
```python
with open(real_file, "r", encoding="utf-8") as f: #打开文件，以读模式，utf-8可以读取中文 
                lines = f.readlines()  # 读取文件所有行，存入列表

                # 遍历每一行：从第2行开始，去掉序号
                for line in lines[1:]:
                    line = line.strip()        # 去掉空格、换行符
                    if not line:              # 如果是空行，跳过，继续循环
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

# 贴入代码及人工注释
复制
