#!/bin/bash

# OpenClaw安装和配置脚本
# 在服务器上执行此脚本

echo "========================================="
echo "开始安装OpenClaw..."
echo "========================================="

# 1. 安装OpenClaw
echo "步骤 1: 下载并安装OpenClaw..."
curl -fsSL https://openclaw.ai/install.sh | bash

# 等待安装完成
sleep 2

# 2. 配置OpenClaw使用MiniMax
echo ""
echo "步骤 2: 配置OpenClaw使用MiniMax API..."

# 创建配置目录（如果不存在）
mkdir -p ~/.openclaw

# 写入配置文件
cat > ~/.openclaw/config.json << 'EOF'
{
  "models": {
    "mode": "merge",
    "providers": {
      "minimax": {
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "apiKey": "sk-cp-Nbi2dlVRkZopZqVYdF-hDRcjjF8OCfSlPlzwValPLCN23J3L-kJvmpa-NyV3RIq9lXwz-ryyxbjRGfgAFLpKCtpis9HErPDse7fNrPfj_aE_sWAwFDjeBnA",
        "api": "anthropic-messages",
        "authHeader": true,
        "models": [
          {
            "id": "MiniMax-M2.1",
            "name": "MiniMax M2.1",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 15,
              "output": 60,
              "cacheRead": 2,
              "cacheWrite": 10
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
EOF

echo "配置文件已创建: ~/.openclaw/config.json"

# 3. 验证安装
echo ""
echo "步骤 3: 验证安装..."
if command -v openclaw &> /dev/null; then
    echo "✓ OpenClaw安装成功！"
    openclaw --version
else
    echo "✗ OpenClaw安装失败，请检查错误信息"
    exit 1
fi

# 4. 提示启动网关
echo ""
echo "========================================="
echo "安装完成！"
echo "========================================="
echo ""
echo "要启动OpenClaw网关，请执行："
echo "  openclaw gateway"
echo ""
echo "然后访问: http://127.0.0.1:18789"
echo ""
echo "或者，如果需要在后台运行："
echo "  nohup openclaw gateway > openclaw.log 2>&1 &"
echo ""
