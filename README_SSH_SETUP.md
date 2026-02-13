# SSH MCP 连接问题解决方案

## 问题描述
SSH MCP无法通过密码认证连接到服务器。

## 解决方案

### 方案1：手动安装OpenClaw（推荐）

1. **SSH连接到服务器**
   ```bash
   ssh root@45.136.14.88 -p 61709
   # 密码: Jn4gix0mjDbb
   ```

2. **上传并执行安装脚本**
   
   在本地执行：
   ```powershell
   scp -P 61709 install_openclaw_on_server.sh root@45.136.14.88:~/
   ```
   
   或者在服务器上直接创建脚本并执行：
   ```bash
   # 下载安装脚本
   curl -o install_openclaw.sh https://raw.githubusercontent.com/your-repo/install_openclaw_on_server.sh
   
   # 或者直接复制 install_openclaw_on_server.sh 的内容到服务器
   nano install_openclaw.sh
   # 粘贴脚本内容，保存退出
   
   # 添加执行权限
   chmod +x install_openclaw.sh
   
   # 执行安装
   ./install_openclaw.sh
   ```

3. **启动OpenClaw网关**
   ```bash
   openclaw gateway
   ```

4. **访问Web界面**
   - 本地访问: http://127.0.0.1:18789
   - 如果需要远程访问，可以使用SSH隧道：
     ```powershell
     ssh -L 18789:localhost:18789 root@45.136.14.88 -p 61709
     ```

### 方案2：配置SSH密钥认证

如果想让SSH MCP正常工作，需要配置SSH密钥认证：

1. **在服务器上添加公钥**
   ```bash
   ssh root@45.136.14.88 -p 61709
   # 输入密码: Jn4gix0mjDbb
   
   # 创建.ssh目录
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   
   # 添加公钥
   echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCcv7E2li0M/lyB9AjCeGMTMxkmEdPAQv0XCk36EKAEH/VlfNKzDJdtfzmpM+wTALpAKQCu4UlTw8AWEsbFd/yz3KpFywgS2z++xkM3Urh4bWgCiafL8muZousiy6vZ7ieuYlOjC+d9SlcIlJcABEaxhJHNZQm1NsVmZHy9Vor1gGwHOoIPXrG3gwzmFZsVznlqFAD7YQCZihScKWG62xsVosKOCGyWF8eNtlOVYRKEBH2FPPtajDxJ/Kp9LdLeu4WgQdih3+htIq/AnjXpDnJcTiy5mBIlAysJoATUGJNFHiL2z0UFBM2cHtO1cLL1dR14sdJuGVRrKY//zPRuQ35QIN8coLiLR5EZJlEblGPgdAhrWWDITx9mu79Df9/YLdfLwmmt1FSOGE+KdMCIlbzay+S0dbSPA7UGSmqdT3zgPwjdUnx6jmtxFKYO0Igu8pb0PVkd9pHYb2Pl07Wkfm9MOYY0vZn2gnhBNT4ocZbjoHmS6PQWJiI8wTvHEhbb/l8= administrator@hasee" >> ~/.ssh/authorized_keys
   
   # 设置权限
   chmod 600 ~/.ssh/authorized_keys
   ```

2. **更新MCP配置使用密钥认证**
   
   MCP配置已经设置为使用密钥，重启Kiro后应该可以连接。

## OpenClaw配置详情

配置文件位置: `~/.openclaw/config.json`

```json
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
```

## 常用命令

```bash
# 启动OpenClaw网关（前台）
openclaw gateway

# 启动OpenClaw网关（后台）
nohup openclaw gateway > openclaw.log 2>&1 &

# 查看OpenClaw日志
tail -f openclaw.log

# 停止OpenClaw
pkill -f "openclaw gateway"

# 查看OpenClaw配置
openclaw config

# 测试MiniMax API连接
curl -X POST https://api.minimaxi.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-cp-Nbi2dlVRkZopZqVYdF-hDRcjjF8OCfSlPlzwValPLCN23J3L-kJvmpa-NyV3RIq9lXwz-ryyxbjRGfgAFLpKCtpis9HErPDse7fNrPfj_aE_sWAwFDjeBnA" \
  -d '{
    "model": "MiniMax-M2.1",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## 故障排查

1. **SSH连接失败**
   - 检查服务器IP和端口是否正确
   - 检查防火墙设置
   - 验证密码或密钥是否正确

2. **OpenClaw安装失败**
   - 检查网络连接
   - 查看安装日志
   - 确保有足够的磁盘空间

3. **MiniMax API调用失败**
   - 验证API Key是否正确
   - 检查baseUrl是否为国内地址: https://api.minimaxi.com/anthropic
   - 确保authHeader设置为true
