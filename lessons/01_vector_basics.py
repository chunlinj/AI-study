"""
第一课：向量基础
目标：理解向量、点积、余弦相似度
"""

import numpy as np

# ============ 第一部分：手动实现 ============

def dot_product(a, b):
    """
    计算两个向量的点积
    提示：对应位置相乘，然后求和
    """
    # TODO: 补全代码
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]

    return result


def vector_length(v):
    """
    计算向量的长度（模）
    提示：各元素平方和，再开根号
    """
    # TODO: 补全代码
    return np.sqrt(np.sum(v ** 2))


def cosine_similarity(a, b):
    """
    计算两个向量的余弦相似度
    提示：点积 / (向量a长度 * 向量b长度)
    """
    dot = np.dot(a, b)
    norm_a = np.sqrt(np.sum(a ** 2))  # 向量 a 的长度
    norm_b = np.sqrt(np.sum(b ** 2))  # 向量 b 的长度
    return dot / (norm_a * norm_b)


# ============ 第二部分：测试你的实现 ============

if __name__ == "__main__":
    # 定义一些动物向量 [体型, 凶猛程度, 可爱程度]
    cat = np.array([0.3, 0.2, 0.9])
    dog = np.array([0.5, 0.4, 0.8])
    tiger = np.array([0.9, 0.95, 0.3])
    rabbit = np.array([0.2, 0.1, 0.95])
    
    print("=== 点积测试 ===")
    print(f"cat · dog = {dot_product(cat, dog)}")
    print(f"cat · tiger = {dot_product(cat, tiger)}")
    
    print("\n=== 向量长度测试 ===")
    print(f"|cat| = {vector_length(cat)}")
    print(f"|tiger| = {vector_length(tiger)}")
    
    print("\n=== 余弦相似度测试 ===")
    print(f"相似度(cat, dog) = {cosine_similarity(cat, dog):.4f}")
    print(f"相似度(cat, tiger) = {cosine_similarity(cat, tiger):.4f}")
    print(f"相似度(cat, rabbit) = {cosine_similarity(cat, rabbit):.4f}")
    
    # 验证：用 NumPy 内置函数对比
    print("\n=== NumPy 验证 ===")
    print(f"np.dot(cat, dog) = {np.dot(cat, dog)}")
    print(f"np.linalg.norm(cat) = {np.linalg.norm(cat):.4f}")


# ============ 第三部分：思考题 ============
"""
1. 为什么余弦相似度比点积更适合比较相似性？

2. 如果两个向量完全相同，余弦相似度是多少？

3. 在 LLM 中，词向量通常有 768 或更多维度，为什么需要这么多维度？

把你的答案写在下面：
---
答案1：
因为余弦相似度有方向，点积没有方向
答案2：
0
答案3：
不知道呀
"""
