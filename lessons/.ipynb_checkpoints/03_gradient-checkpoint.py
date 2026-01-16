"""
第三课：梯度与求导
目标：理解导数、梯度、梯度下降
"""

import numpy as np
import matplotlib.pyplot as plt

# ============ 第一部分：数值求导 ============

def numerical_derivative(f, x, h=1e-5):
    """
    数值求导：用极限定义计算导数
    
    导数定义：f'(x) = lim(h→0) [f(x+h) - f(x)] / h
    
    我们用一个很小的 h 来近似
    """
    return (f(x + h) - f(x)) / h


# 测试：f(x) = x²，导数应该是 2x
def f1(x):
    return x ** 2

print("=== 数值求导测试 ===")
print(f"f(x) = x²")
print(f"f'(3) 数值计算 = {numerical_derivative(f1, 3):.4f}")
print(f"f'(3) 解析解 = {2 * 3}")  # 导数 2x，x=3 时是 6


# ============ 第二部分：多变量的梯度 ============

def numerical_gradient(f, params, h=1e-5):
    """
    计算多变量函数的梯度
    
    梯度 = [∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ]
    
    对每个变量分别求偏导数
    """
    grad = np.zeros_like(params)
    
    for i in range(len(params)):
        # 保存原值
        original = params[i]
        
        # 计算 f(x + h)
        params[i] = original + h
        fxh1 = f(params)
        
        # 计算 f(x - h)
        params[i] = original - h
        fxh2 = f(params)
        
        # 中心差分法（更精确）
        grad[i] = (fxh1 - fxh2) / (2 * h)
        
        # 恢复原值
        params[i] = original
    
    return grad


# 测试：f(x, y) = x² + y²
def f2(params):
    x, y = params
    return x ** 2 + y ** 2

print("\n=== 梯度测试 ===")
print(f"f(x, y) = x² + y²")
params = np.array([3.0, 4.0])
grad = numerical_gradient(f2, params)
print(f"在点 (3, 4) 的梯度 = {grad}")
print(f"解析解 = [2x, 2y] = [6, 8]")


# ============ 第三部分：梯度下降 ============

def gradient_descent(f, initial_params, learning_rate=0.1, iterations=50):
    """
    梯度下降算法：找函数的最小值
    
    核心公式：params = params - learning_rate * gradient
    
    就像下山：每一步都往最陡的下坡方向走
    """
    params = initial_params.copy()
    history = [params.copy()]
    
    for i in range(iterations):
        grad = numerical_gradient(f, params)
        params = params - learning_rate * grad
        history.append(params.copy())
        
        if i % 10 == 0:
            print(f"迭代 {i}: params = {params}, f = {f(params):.4f}")
    
    return params, history


print("\n=== 梯度下降找最小值 ===")
print("目标：找 f(x, y) = x² + y² 的最小值点")
print("起点：(5, 5)")

initial = np.array([5.0, 5.0])
final, history = gradient_descent(f2, initial, learning_rate=0.1, iterations=50)

print(f"\n最终结果：{final}")
print(f"最小值：{f2(final):.6f}")
print("（理论最小值在 (0, 0)，值为 0）")


# ============ 第四部分：可视化 ============

if __name__ == "__main__":
    # 绘制梯度下降过程
    history = np.array(history)
    
    plt.figure(figsize=(10, 4))
    
    # 左图：下降路径
    plt.subplot(1, 2, 1)
    plt.plot(history[:, 0], history[:, 1], 'b.-', markersize=10)
    plt.plot(5, 5, 'go', markersize=15, label='起点')
    plt.plot(final[0], final[1], 'r*', markersize=15, label='终点')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('梯度下降路径')
    plt.legend()
    plt.grid(True)
    
    # 右图：函数值变化
    plt.subplot(1, 2, 2)
    values = [f2(h) for h in history]
    plt.plot(values, 'b.-')
    plt.xlabel('迭代次数')
    plt.ylabel('f(x, y)')
    plt.title('函数值下降过程')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('lessons/03_gradient_descent.png')
    print("\n图片已保存到 lessons/03_gradient_descent.png")
