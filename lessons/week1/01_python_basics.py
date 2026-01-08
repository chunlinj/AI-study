"""
第1周 - 1.1 Python 快速入门（Java 转 Python）
目标：掌握 Python 与 Java 的核心差异
"""

# ============ 1. 基础语法差异 ============

# Java: int x = 10;
# Python: 动态类型，不需要声明类型
x = 10
name = "张三"
is_active = True

print(f"x = {x}, 类型: {type(x)}")
print(f"name = {name}, 类型: {type(name)}")

# 类型可以随时改变（Java 做不到）
x = "现在我是字符串了"
print(f"x 变成了: {x}")


# ============ 2. 缩进代替大括号 ============

# Java:
# if (score >= 60) {
#     System.out.println("及格");
# } else {
#     System.out.println("不及格");
# }

# Python: 用缩进表示代码块（通常 4 个空格）
score = 75
if score >= 60:
    print("及格")
    print("继续努力")  # 同一缩进级别 = 同一代码块
else:
    print("不及格")


# ============ 3. 循环 ============

# Java: for (int i = 0; i < 5; i++)
# Python: range(5) 生成 0,1,2,3,4
print("\n=== for 循环 ===")
for i in range(5):
    print(f"i = {i}")

# 遍历列表（Java 的 for-each）
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"水果: {fruit}")

# 带索引遍历
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")


# ============ 4. 列表（类似 Java ArrayList） ============

print("\n=== 列表操作 ===")
numbers = [1, 2, 3, 4, 5]

# 添加元素
numbers.append(6)        # Java: list.add(6)
print(f"append 后: {numbers}")

# 切片（Python 特有，超好用！）
print(f"前3个: {numbers[:3]}")      # [1, 2, 3]
print(f"后3个: {numbers[-3:]}")     # [4, 5, 6]
print(f"第2到4个: {numbers[1:4]}")  # [2, 3, 4]


# ============ 5. 列表推导式（Python 精华！） ============

print("\n=== 列表推导式 ===")

# Java 写法：
# List<Integer> squares = new ArrayList<>();
# for (int i = 1; i <= 5; i++) {
#     squares.add(i * i);
# }

# Python 一行搞定：
squares = [i ** 2 for i in range(1, 6)]
print(f"平方数: {squares}")

# 带条件的列表推导式
evens = [i for i in range(10) if i % 2 == 0]
print(f"偶数: {evens}")

# 实际应用：处理数据
words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]
print(f"大写: {upper_words}")


# ============ 6. 字典（类似 Java HashMap） ============

print("\n=== 字典操作 ===")
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

print(f"姓名: {person['name']}")
print(f"年龄: {person.get('age')}")  # get 方法更安全

# 遍历字典
for key, value in person.items():
    print(f"{key}: {value}")


# ============ 7. 函数定义 ============

print("\n=== 函数 ===")

# Java:
# public int add(int a, int b) {
#     return a + b;
# }

# Python:
def add(a, b):
    """这是文档字符串，描述函数功能"""
    return a + b

print(f"3 + 5 = {add(3, 5)}")

# 默认参数（Java 没有）
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

print(greet("张三"))
print(greet("张三", "早上好"))

# 返回多个值（Java 需要封装成对象）
def get_min_max(numbers):
    return min(numbers), max(numbers)

min_val, max_val = get_min_max([3, 1, 4, 1, 5, 9])
print(f"最小: {min_val}, 最大: {max_val}")


# ============ 8. 异常处理 ============

print("\n=== 异常处理 ===")

# Java: try-catch-finally
# Python: try-except-finally

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"捕获异常: {e}")
finally:
    print("finally 块总会执行")


# ============ 练习题 ============
"""
练习1：用列表推导式生成 1-100 中所有能被 3 整除的数

练习2：写一个函数，接收一个字符串列表，返回最长的字符串

练习3：创建一个字典，存储 3 个学生的姓名和成绩，然后计算平均分

把你的代码写在下面：
---
"""

# 练习1：1-100 中能被 3 整除的数
divisible_by_3 = [i for i in range(1, 101) if i % 3 == 0]
print(f"被 3 整除的数: {divisible_by_3}")

# 练习2：返回最长的字符串
def find_longest(str_list):
    """接收字符串列表，返回最长的字符串"""
    longest = ""
    for s in str_list:  # 直接遍历列表，不需要 range(len())
        if len(s) > len(longest):
            longest = s
    return longest

# 测试练习2
test_words = ["casa", "acascasc", "aa"]
print(f"最长字符串: {find_longest(test_words)}")

# 更 Pythonic 的写法（一行）：
# longest = max(str_list, key=len)

# 练习3：学生成绩平均分
students = [
    {"name": "张三", "score": 27},
    {"name": "李四", "score": 25},
    {"name": "王五", "score": 21}
]

total = 0  # 先初始化变量
for student in students:  # 直接遍历列表
    total += student["score"]  # += 中间不能有空格

average = total / len(students)
print(f"平均分: {average}")

# 更 Pythonic 的写法（一行）：
# average = sum(s["score"] for s in students) / len(students)

