# LifeMaster 云端部署指南 - Sealos Cloud 数据库部署

## 🎯 部署目标
- ✅ 使用 Sealos Cloud 部署 MySQL 数据库
- ✅ 获得稳定的云端数据库服务
- ✅ 国内直接访问，**无需VPN**
- ✅ 完全**免费**的数据库托管

## 🚀 Sealos Cloud MySQL 部署教程

### **为什么选择 Sealos Cloud？**
- ✅ **国内云服务** - 访问速度快，无需VPN
- ✅ **一键部署** - MySQL数据库快速创建
- ✅ **免费额度** - 新用户赠送免费使用时长
- ✅ **简单易用** - 可视化管理界面

---

## 📋 Sealos Cloud 部署教程

### **第一步：注册 Sealos Cloud 账号**

#### 1.1 访问官网注册
- 访问：https://cloud.sealos.io/
- 点击 "免费试用" 或 "立即注册"
- 支持微信、GitHub等方式注册
- 新用户自动赠送免费额度

#### 1.2 完成实名认证
- 登录后根据提示完成实名认证
- 认证通过后可获得更多免费额度

### **第二步：创建 MySQL 数据库**

#### 2.1 进入应用市场
1. **登录 Sealos 控制台**
2. **点击 "应用市场"**
3. **搜索 "MySQL"** 或直接找到 MySQL 应用图标

#### 2.2 配置 MySQL 参数
选择 MySQL 应用后，配置以下参数：

```yaml
应用名称: lifemaster-db
MySQL版本: 8.0
存储大小: 1GB (免费额度内)
CPU配置: 0.1核 (免费额度内)
内存配置: 128Mi (免费额度内)
```

#### 2.3 设置数据库账户
```env
数据库root密码: LifeMaster123!@#
数据库名称: lifemaster
用户名: lifemaster_user
用户密码: LifeMaster2025!
```

#### 2.4 一键部署
- 检查配置无误后点击 "立即部署"
- 等待2-3分钟完成部署
- 部署成功后会显示数据库状态为"运行中"

### **第三步：获取数据库连接信息**

#### 3.1 查看连接信息
1. **在 Sealos 控制台找到已部署的 MySQL 应用**
2. **点击应用名称进入详情页**
3. **查看 "网络" 或 "连接信息" 标签页**
4. **复制外网访问地址**

#### 3.2 连接信息格式
Sealos 提供的连接信息通常格式为：
```
主机地址: xxx.sealos.run
端口: 3306
数据库名: lifemaster
用户名: lifemaster_user
密码: LifeMaster2025!
```

#### 3.3 构建完整连接字符串
将连接信息组合成Flask需要的格式：
```env
DATABASE_URL=mysql+pymysql://lifemaster_user:LifeMaster2025!@xxx.sealos.run:3306/lifemaster?charset=utf8mb4
```

### **第四步：测试数据库连接**

#### 4.1 在线测试连接
1. **在 Sealos 控制台点击 "终端" 按钮**
2. **进入 MySQL 容器内部**
3. **执行连接测试**：
```bash
mysql -u lifemaster_user -p
# 输入密码: LifeMaster2025!
```

#### 4.2 创建应用数据库（如果需要）
```sql
-- 在MySQL终端中执行
CREATE DATABASE IF NOT EXISTS lifemaster CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
USE lifemaster;
```

### **第五步：在应用中使用数据库**

#### 5.1 设置环境变量
在你的Flask应用中，使用获得的连接字符串：
```env
DATABASE_URL=mysql+pymysql://lifemaster_user:LifeMaster2025!@xxx.sealos.run:3306/lifemaster?charset=utf8mb4
```

#### 5.2 验证连接
在Flask应用中测试数据库连接：
```python
# 在app.py中添加测试路由
@app.route('/api/test-db', methods=['GET'])
def test_database():
    try:
        from sqlalchemy import text
        result = db.session.execute(text("SELECT 1"))
        return jsonify({
            "code": 0,
            "msg": "数据库连接成功",
            "data": {"status": "connected"}
        })
    except Exception as e:
        return jsonify({
            "code": -1,
            "msg": f"数据库连接失败: {str(e)}"
        }), 500
```

---

## 💰 Sealos Cloud 免费额度说明

### **免费资源配置**
- 💰 **新用户赠金** - 注册即送10-50元免费额度
- 🗄️ **存储空间** - 1GB存储空间
- ⚡ **计算资源** - 0.1核CPU + 128Mi内存
- ⏰ **使用时长** - 根据配置每小时消耗约0.1-0.5元

### **费用计算**
```
每小时费用 ≈ 0.2元
每天费用 ≈ 4.8元
免费额度可用时长 ≈ 10-25天
```

### **节省费用技巧**
- 🔄 **按需使用** - 开发时开启，不用时暂停
- 📉 **优化配置** - 根据实际需求调整资源
- 🕒 **定期检查** - 监控费用使用情况

---

## 🔧 数据库管理

### **Sealos 管理功能**
- **📊 监控面板** - 实时查看数据库状态、CPU、内存使用
- **💻 在线终端** - 直接连接MySQL执行SQL命令
- **📋 日志查看** - 查看数据库运行日志和错误信息
- **⚙️ 配置管理** - 在线修改数据库配置参数

### **数据备份**
```sql
-- 手动备份重要数据
mysqldump -u lifemaster_user -p lifemaster > backup.sql

-- 或使用Sealos的自动备份功能
-- 在控制台设置定期备份策略
```

### **性能优化**
```sql
-- 添加常用索引提升查询性能
ALTER TABLE tasks ADD INDEX idx_user_id (user_id);
ALTER TABLE tasks ADD INDEX idx_deadline (deadline);
ALTER TABLE accounting_records ADD INDEX idx_user_date (user_id, date);
ALTER TABLE handbooks ADD INDEX idx_user_updated (user_id, updated_at);
```

---

## 🆘 常见问题解决

### **Q: 无法连接到数据库？**
```bash
A: 检查以下项目：
1. 确认数据库状态为"运行中"
2. 检查连接字符串格式：mysql+pymysql://user:pass@host:port/db?charset=utf8mb4
3. 确认网络可以访问外网
4. 检查用户名密码是否正确
```

### **Q: 连接字符串格式错误？**
```bash
A: 正确格式示例：
DATABASE_URL=mysql+pymysql://lifemaster_user:LifeMaster2025!@abc123.sealos.run:3306/lifemaster?charset=utf8mb4

注意事项：
- 必须添加 +pymysql
- 必须添加 ?charset=utf8mb4
- 密码中的特殊字符需要URL编码
```

### **Q: 免费额度用完怎么办？**
```bash
A: 解决方案：
1. 充值继续使用（推荐）
2. 暂停数据库，导出数据到本地
3. 重新注册账号（不推荐）
4. 切换到其他免费数据库服务
```

### **Q: 数据库性能慢？**
```bash
A: 优化建议：
1. 添加合适的索引
2. 优化SQL查询语句
3. 升级数据库配置（增加CPU/内存）
4. 定期清理无用数据
```

---

## 🎯 下一步操作

### **完成数据库部署后：**
1. ✅ **记录连接信息** - 保存数据库连接字符串
2. ✅ **测试连接** - 确认应用可以正常连接数据库
3. ✅ **初始化数据表** - 运行 `/api/admin/init-db` 创建表结构
4. ✅ **部署后端应用** - 使用 Render 等平台部署Flask后端
5. ✅ **配置前端** - 更新前端API地址

### **数据库连接字符串示例：**
```env
# 将此字符串添加到你的部署平台环境变量中
DATABASE_URL=mysql+pymysql://lifemaster_user:LifeMaster2025!@your-host.sealos.run:3306/lifemaster?charset=utf8mb4
```

**🌟 现在你已经拥有了一个稳定的云端MySQL数据库！**

接下来可以继续部署Flask后端应用，将数据库连接字符串配置到后端环境变量中即可。