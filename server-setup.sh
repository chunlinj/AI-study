#!/bin/bash
# AI Agent 服务器一键安装脚本
# 适用于 Debian 12

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  AI Agent 服务器一键安装脚本"
echo "=========================================="

# 1. 更新系统
echo "[1/8] 更新系统..."
apt update && apt upgrade -y

# 2. 安装基础工具
echo "[2/8] 安装基础工具..."
apt install -y curl wget git vim htop unzip

# 3. 安装 Docker
echo "[3/8] 安装 Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
else
    echo "Docker 已安装，跳过"
fi

# 4. 安装 Docker Compose
echo "[4/8] 安装 Docker Compose..."
apt install -y docker-compose-plugin

# 5. 创建 Swap
echo "[5/8] 创建 8G Swap..."
if [ ! -f /swapfile ]; then
    fallocate -l 8G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap 创建成功"
else
    echo "Swap 已存在，跳过"
fi

# 6. 安装 Node.js
echo "[6/8] 安装 Node.js 20..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
else
    echo "Node.js 已安装，跳过"
fi

# 7. 安装 Python
echo "[7/8] 安装 Python 环境..."
apt install -y python3 python3-pip python3-venv

# 8. 安装 Open WebUI
echo "[8/8] 安装 Open WebUI..."
mkdir -p /opt/ai-agent && cd /opt/ai-agent

if ! docker ps -a | grep -q open-webui; then
    docker run -d \
        --name open-webui \
        --restart always \
        -p 3000:8080 \
        -v open-webui-data:/app/backend/data \
        ghcr.io/open-webui/open-webui:main
    echo "Open WebUI 安装成功"
else
    echo "Open WebUI 已存在，跳过"
fi

# 配置防火墙
echo "[额外] 配置防火墙..."
apt install -y ufw
ufw allow 61709/tcp   # SSH
ufw allow 3000/tcp    # Open WebUI
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
echo "y" | ufw enable

# 安装 fail2ban
apt install -y fail2ban
systemctl enable fail2ban

echo ""
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo ""
echo "服务器信息："
echo "  - Docker: $(docker --version)"
echo "  - Node.js: $(node --version)"
echo "  - Python: $(python3 --version)"
echo ""
echo "内存状态："
free -h
echo ""
echo "磁盘状态："
df -h /
echo ""
echo "运行的容器："
docker ps
echo ""
echo "=========================================="
echo "  访问地址: http://$(curl -s ifconfig.me):3000"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 在浏览器打开上面的地址"
echo "2. 注册管理员账号"
echo "3. 在设置中配置 Claude API Key"
echo ""
