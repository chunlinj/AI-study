"""
第四课：概率基础
目标：理解 softmax、交叉熵损失
"""

import numpy as np

# ============ 第一部分：Softmax ============

"""
问题：神经网络输出的是任意数字，比如 [2.0, 1.0, 0.1]
我们想把它变成概率（和为1，每个值在0-1之间）

Softmax 公式：
    softmax(x_i) = e^(x_i) / Σ e^(x_j)
    
就是：每个数取 e 的指数，然后除以所有指数的和
"""

def softmax(x):
    """
    将任意数值转换为概率分布
    """
    exp_x = np.exp(x)           # 对每个元素取 e^x
    return exp_x / np.sum(exp_x) # 除以总和，使得和为 1


# 测试
print("=== Softmax 测试 ===")
logits = np.array([2.0, 1.0, 0.1])  # 神经网络的原始输出（叫 logits）
probs = softmax(logits)

print(f"原始输出 (logits): {logits}")
print(f"Softmax 后 (概率): {probs}")
print(f"概率之和: {np.sum(probs):.4f}")  # 应该是 1


# ============ 第二部分：为什么用 e^x？ ============

"""
为什么不直接用 x / sum(x)？

1. 原始值可能是负数，负数不能当概率
2. e^x 永远是正数
3. e^x 会放大差异：大的更大，小的更小
   - 让模型更"自信"地做出选择
"""

print("\n=== e^x 的效果 ===")
x = np.array([-1, 0, 1, 2])
print(f"原始值: {x}")
print(f"e^x:    {np.exp(x)}")


# ============ 第三部分：交叉熵损失 ============

"""
现在我们有了预测概率，怎么衡量预测的好坏？

假设：
- 真实标签：这是一只猫（类别 0）
- 预测概率：[0.7, 0.2, 0.1]（猫、狗、鸟）

交叉熵损失 = -log(预测正确类别的概率)
           = -log(0.7)
           ≈ 0.36

如果预测概率是 [0.1, 0.8, 0.1]（预测成狗了）
交叉熵损失 = -log(0.1) ≈ 2.30（损失更大！）
"""

def cross_entropy_loss(probs, target_index):
    """
    计算交叉熵损失
    
    probs: 预测的概率分布
    target_index: 正确答案的索引
    """
    return -np.log(probs[target_index])


print("\n=== 交叉熵损失测试 ===")

# 场景1：预测正确（猫的概率最高）
probs_good = np.array([0.7, 0.2, 0.1])  # 猫、狗、鸟
target = 0  # 真实是猫
loss_good = cross_entropy_loss(probs_good, target)
print(f"预测概率: {probs_good}, 真实: 猫(0)")
print(f"损失: {loss_good:.4f}")

# 场景2：预测错误（狗的概率最高）
probs_bad = np.array([0.1, 0.8, 0.1])
loss_bad = cross_entropy_loss(probs_bad, target)
print(f"\n预测概率: {probs_bad}, 真实: 猫(0)")
print(f"损失: {loss_bad:.4f}")

print(f"\n结论：预测错误时损失更大 ({loss_bad:.2f} > {loss_good:.2f})")


# ============ 第四部分：完整流程 ============

"""
神经网络分类的完整流程：

1. 网络输出 logits（任意数值）
2. Softmax 转成概率
3. 交叉熵计算损失
4. 梯度下降优化，让损失变小
"""

def classify_and_compute_loss(logits, target_index):
    """
    完整的分类损失计算
    """
    probs = softmax(logits)
    loss = cross_entropy_loss(probs, target_index)
    return probs, loss


print("\n=== 完整流程演示 ===")
# 假设网络输出
logits = np.array([2.5, 1.0, 0.5])  # 三个类别的得分
target = 0  # 真实标签是类别 0

probs, loss = classify_and_compute_loss(logits, target)
print(f"网络输出 (logits): {logits}")
print(f"预测概率: {probs}")
print(f"预测类别: {np.argmax(probs)} (概率最大的)")
print(f"真实类别: {target}")
print(f"损失: {loss:.4f}")


# ============ 第五部分：思考题 ============
"""
1. 如果预测概率是 [1.0, 0.0, 0.0]，真实标签是 0，损失是多少？

2. 如果预测概率是 [0.33, 0.33, 0.34]（几乎均匀），损失大概是多少？

3. 为什么用 -log 而不是直接用 (1 - 预测概率) 作为损失？

把你的答案写在下面：
---
答案1：

答案2：

答案3：

"""
