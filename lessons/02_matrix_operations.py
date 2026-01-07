"""
第二课：矩阵运算
目标：理解矩阵、矩阵乘法、转置
"""

import numpy as np

# ============ 第一部分：矩阵基础 ============

# 创建矩阵
A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])  # 2x3 矩阵

B = np.array([
    [7, 8],
    [9, 10],
    [11, 12]
])  # 3x2 矩阵

print("矩阵 A (2x3):")
print(A)
print(f"形状: {A.shape}")  # shape 是 NumPy 的属性，返回 (行数, 列数)

print("\n矩阵 B (3x2):")
print(B)
print(f"形状: {B.shape}")


# ============ 第二部分：手动实现矩阵乘法 ============

def matrix_multiply(A, B):
    """
    矩阵乘法：A(m×n) × B(n×p) = C(m×p)
    
    规则：C[i][j] = A 的第 i 行 与 B 的第 j 列 的点积
    """
    m = len(A)      # A 的行数
    n = len(A[0])   # A 的列数
    p = len(B[0])   # B 的列数
    
    # 检查维度是否匹配（Python 用 raise 抛异常，不是 throw）
    if n != len(B):
        raise ValueError(f"维度不匹配: A 的列数({n}) != B 的行数({len(B)})")
    
    # 创建结果矩阵，初始化为 0
    # Python 列表推导式：创建 m 行 p 列的二维数组
    C = [[0 for _ in range(p)] for _ in range(m)]
    
    # 三层循环计算（和 Java 一样的逻辑）
    for i in range(m):          # 遍历 A 的每一行
        for j in range(p):      # 遍历 B 的每一列
            for k in range(n):  # 计算点积
                C[i][j] += A[i][k] * B[k][j]
    
    return np.array(C)


# ============ 第三部分：矩阵转置 ============

def transpose(A):
    """
    矩阵转置：行变列，列变行
    
    例如：
    [[1, 2, 3],      [[1, 4],
     [4, 5, 6]]  →    [2, 5],
                      [3, 6]]
    """
    m = len(A)      # 原矩阵行数
    n = len(A[0])   # 原矩阵列数
    
    # 转置后：n 行 m 列
    T = [[0 for _ in range(m)] for _ in range(n)]
    
    for i in range(m):
        for j in range(n):
            T[j][i] = A[i][j]  # 关键：行列互换
    
    return np.array(T)


# ============ 第四部分：测试 ============

if __name__ == "__main__":
    print("\n=== 矩阵乘法测试 ===")
    
    # 手动计算验证：
    # C[0][0] = 1*7 + 2*9 + 3*11 = 7 + 18 + 33 = 58
    # C[0][1] = 1*8 + 2*10 + 3*12 = 8 + 20 + 36 = 64
    # ...
    
    C = matrix_multiply(A, B)
    print("手动实现结果:")
    print(C)
    
    print("\nNumPy 验证 (np.matmul):")
    print(np.matmul(A, B))
    
    print("\n=== 转置测试 ===")
    print("原矩阵 A:")
    print(A)
    print("\n转置后:")
    print(transpose(A))
    print("\nNumPy 验证 (A.T):")
    print(A.T)


# ============ 第五部分：思考题 ============
"""
1. 为什么矩阵乘法要求 A 的列数等于 B 的行数？

2. 神经网络中，输入是 [batch_size, input_dim]，权重是 [input_dim, output_dim]，
   输出的形状是什么？

3. 如果 A 是 (2, 3)，B 是 (2, 3)，能直接相乘吗？如果想乘，该怎么办？

把你的答案写在下面：
---
答案1：
因为需要用A的列数去乘以B的行数，如果不相等则计算会缺失数据去计算
答案2：
不知道啊，这个是用矩阵相乘去计算吗？如果是的，那么就是 batch_size*output_dim  
答案3：
不能，B 的列数3改为2即可
"""
