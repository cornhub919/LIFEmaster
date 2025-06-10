# LifeMaster 跨机器部署指南

## 🌐 当前状态分析

### **本地部署限制**
目前的配置只能在本地使用，无法跨机器访问：

```
你的电脑 💻
├── MySQL数据库 (localhost)
├── Flask服务器 (localhost:5000)
└── 前端页面 (file://)

其他电脑 💻 ❌ 无法访问
```

**限制原因：**
- 数据库在本地 - MySQL只在你的电脑上
- Flask服务器本地运行 - 只监听 `localhost:5000`
- 网络隔离 - 其他电脑无法访问你的本地服务

## 🔧 解决方案

### 部署方案难度评级

| 方案         | 难度      | 预计耗时         | 适用场景                   |
| ------------ | --------- | ---------------- | -------------------------- |
| 局域网共享   | ★☆☆☆☆    | 0.5~1天          | 局域网测试、同寝室/同WiFi  |
| 云服务器部署 | ★★★★☆    | 1~2天            | 长期运行、对外服务、生产环境|
| 混合部署     | ★★☆☆☆    | 0.5~1天          | 本地开发+多人协作          |

> **建议**：开发/测试阶段优先用局域网或混合部署，正式上线推荐云服务器部署。

### **方案一：局域网共享（适合同寝室/同WiFi测试）**

#### 1. 修改Flask配置，允许外部访问
```python
# 在 app.py 最后修改
if __name__ == '__main__':
    # 修改前：app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)  # 允许外部访问
```

#### 2. 获取本机IP地址
```cmd
ipconfig
```
找到类似 `192.168.1.xxx` 的内网IP地址

#### 3. 修改前端API地址
```javascript
// 在 前端/scripts.js 中修改第一行
// 修改前：const API_BASE_URL = 'http://localhost:5000';
const API_BASE_URL = 'http://192.168.1.xxx:5000';  // 替换为你的实际IP
```

#### 4. 配置MySQL允许外部连接
```sql
-- 登录MySQL
mysql -u root -p

-- 创建允许远程访问的用户
CREATE USER 'lifemaster'@'%' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON lifemaster.* TO 'lifemaster'@'%';
FLUSH PRIVILEGES;
```

#### 5. 修改数据库配置
```env
# 在 .env 文件中修改
DB_HOST=192.168.1.xxx  # 你的IP地址
DB_USER=lifemaster
DB_PASSWORD=password123
```

#### 6. 测试局域网访问
1. **在你的电脑上启动服务**：`python app.py`
2. **在其他电脑上访问**：`http://192.168.1.xxx:5000`
3. **或者直接访问前端页面**，确保前端能调用API

**局域网方案的特点：**
- ✅ 同一WiFi下的设备可以访问
- ✅ 配置简单，适合测试
- ❌ 不同网络无法访问
- ❌ 电脑关机后服务停止
- ⚠️ 数据安全性较低

---

### **方案二：云服务器部署（推荐生产环境）**

#### 免费云服务选择

**1. 腾讯云（推荐学生）**
- 学生认证后有优惠
- 轻量应用服务器
- 免费的云数据库MySQL

**2. 阿里云**
- 免费试用额度
- ECS云服务器
- RDS数据库服务

**3. Railway（推荐快速部署）**
- GitHub集成
- 免费额度充足
- 自动部署和扩容

**4. Heroku + PlanetScale**
- Heroku：免费应用托管
- PlanetScale：免费MySQL云数据库

#### 云部署步骤（以Railway为例）

**1. 准备代码**
```bash
# 创建requirements.txt
pip freeze > requirements.txt

# 创建Procfile
echo "web: python app.py" > Procfile
```

**2. 修改app.py支持云部署**
```python
import os

# ...existing code...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**3. 配置环境变量**
```env
# 云数据库配置
DB_HOST=your-cloud-db-host
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=lifemaster
JWT_SECRET_KEY=your-production-secret-key
```

**4. 部署流程**
1. 注册Railway账号
2. 连接GitHub仓库
3. 配置环境变量
4. 自动部署

#### 云数据库配置

**PlanetScale（推荐）**
```bash
# 1. 注册PlanetScale账号
# 2. 创建数据库
# 3. 获取连接字符串
# 4. 配置环境变量
```

**腾讯云MySQL**
```bash
# 1. 开通云数据库MySQL
# 2. 创建数据库实例
# 3. 设置访问权限
# 4. 获取连接信息
```

**云部署的优势：**
- ✅ 任何地方都能访问
- ✅ 24小时在线服务
- ✅ 专业的数据备份
- ✅ 更好的安全性
- ✅ 支持自定义域名
- ✅ 自动扩容和负载均衡

---

### **方案三：混合部署（开发推荐）**

**本地开发 + 云数据库**
```env
# 使用云数据库，本地运行服务
DB_HOST=your-cloud-db-host
DB_USER=cloud-user
DB_PASSWORD=cloud-password
DB_NAME=lifemaster
```

**优势：**
- 开发时使用本地服务器（快速调试）
- 数据存储在云端（多人共享）
- 随时可以部署到云服务器

## 🚀 推荐发展路线

1. **第一阶段：本地开发** ✅ 已完成
   - 功能开发和测试
   - 数据库设计完善

2. **第二阶段：局域网测试**
   - 室友/同学测试
   - 发现多用户问题

3. **第三阶段：云端部署**
   - 正式上线
   - 对外提供服务

## 📋 部署检查清单

### **局域网部署**
- [ ] 修改Flask监听地址为 `0.0.0.0`
- [ ] 获取本机IP地址
- [ ] 修改前端API_BASE_URL
- [ ] 配置MySQL外部访问
- [ ] 测试其他设备访问

### **云部署**
- [ ] 选择云服务提供商
- [ ] 准备部署文件（requirements.txt, Procfile等）
- [ ] 配置云数据库
- [ ] 设置环境变量
- [ ] 部署应用
- [ ] 测试线上访问
- [ ] 配置域名（可选）

## 💡 部署建议

### **开发阶段**
- 使用本地MySQL + 本地Flask
- 快速迭代和调试

### **测试阶段**
- 使用局域网部署
- 多人测试验证功能

### **生产阶段**
- 使用云服务器 + 云数据库
- 稳定的在线服务

## 🔐 安全注意事项

### **局域网部署**
- 修改默认密码
- 限制访问IP范围
- 关闭调试模式

### **云部署**
- 使用HTTPS
- 强密码和密钥
- 定期备份数据
- 监控异常访问

选择适合你当前需求的部署方案，随着项目发展逐步升级！