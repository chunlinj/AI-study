"""
简单的 MCP Server 示例
使用 fastmcp 库创建

安装依赖：pip install fastmcp
运行方式：python mcp_server_simple.py
"""

try:
    from fastmcp import FastMCP
except ImportError:
    print("请先安装 fastmcp: pip install fastmcp")
    exit(1)

from datetime import datetime

# 创建 MCP Server 实例
mcp = FastMCP("我的工具箱")


# ============ 工具定义 ============

@mcp.tool()
def get_current_time() -> str:
    """获取当前日期和时间"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@mcp.tool()
def calculate(expression: str) -> str:
    """
    计算数学表达式
    
    Args:
        expression: 数学表达式，如 "(2+3)*4" 或 "2**10"
    """
    try:
        # 安全检查：只允许数字和基本运算符
        allowed = set("0123456789+-*/().** ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"{expression} = {result}"
        return "错误：表达式包含不允许的字符"
    except Exception as e:
        return f"计算错误: {e}"


@mcp.tool()
def get_weather(city: str) -> str:
    """
    查询城市天气（模拟数据）
    
    Args:
        city: 城市名称，如 "北京"、"上海"
    """
    weather_data = {
        "北京": {"temp": -2, "text": "晴", "wind": "北风3级", "humidity": 30},
        "上海": {"temp": 8, "text": "多云", "wind": "东风2级", "humidity": 65},
        "深圳": {"temp": 18, "text": "晴", "wind": "南风2级", "humidity": 70},
        "广州": {"temp": 15, "text": "阴", "wind": "东南风1级", "humidity": 75},
        "天津": {"temp": -3, "text": "晴", "wind": "西北风3级", "humidity": 35},
        "成都": {"temp": 6, "text": "多云", "wind": "微风", "humidity": 80},
    }
    
    if city in weather_data:
        w = weather_data[city]
        return f"{city}天气：{w['text']}，温度 {w['temp']}°C，{w['wind']}，湿度 {w['humidity']}%"
    
    return f"暂无 {city} 的天气数据。支持的城市：{', '.join(weather_data.keys())}"


@mcp.tool()
def search_product(name: str, max_price: float = None) -> str:
    """
    搜索商品信息（模拟数据）
    
    Args:
        name: 商品名称或关键词
        max_price: 最高价格限制（可选）
    """
    products = {
        "iphone": {"name": "iPhone 15", "price": 5999, "stock": 100},
        "macbook": {"name": "MacBook Pro", "price": 12999, "stock": 50},
        "airpods": {"name": "AirPods Pro", "price": 1899, "stock": 200},
        "ipad": {"name": "iPad Air", "price": 4599, "stock": 80},
        "watch": {"name": "Apple Watch", "price": 2999, "stock": 120},
    }
    
    name_lower = name.lower()
    for key, product in products.items():
        if key in name_lower or name_lower in key:
            if max_price and product["price"] > max_price:
                return f"找到 {product['name']}，价格 {product['price']} 元，超出预算 {max_price} 元"
            return f"商品：{product['name']}，价格：{product['price']} 元，库存：{product['stock']} 件"
    
    return f"未找到商品：{name}。支持搜索：iPhone, MacBook, AirPods, iPad, Watch"


@mcp.tool()
def get_word_length(text: str) -> str:
    """
    获取文本的字符长度
    
    Args:
        text: 要计算长度的文本
    """
    return f"'{text}' 的长度是 {len(text)} 个字符"


# ============ 资源定义 ============

@mcp.resource("config://server-info")
def get_server_info() -> str:
    """服务器信息"""
    return """
{
    "name": "简单MCP工具箱",
    "version": "1.0.0",
    "author": "AI学习者",
    "tools": ["时间查询", "计算器", "天气查询", "商品搜索", "字符计数"]
}
"""


# ============ 运行服务器 ============

if __name__ == "__main__":
    print("启动 MCP Server...")
    print("支持的工具：")
    print("  - get_current_time: 获取当前时间")
    print("  - calculate: 计算数学表达式")
    print("  - get_weather: 查询天气")
    print("  - search_product: 搜索商品")
    print("  - get_word_length: 计算字符长度")
    print("\n按 Ctrl+C 停止服务器")
    
    mcp.run()
