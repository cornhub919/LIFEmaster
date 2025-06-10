# LifeMaster 数据库配置指南

## 📋 环境准备

### 1. 安装依赖
```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors pymysql python-dotenv
```

### 2. 环境配置
创建 `.env` 文件：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=lifemaster
JWT_SECRET_KEY=your-secret-key-123
```

## 🗄️ MySQL 数据库设置

### 1. 启动 MySQL 服务
```bash
# Windows
net start mysql

# 验证服务
mysql --version
```

### 2. 创建数据库
```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE lifemaster CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
exit;
```

### 3. 测试连接
```bash
# 测试数据库连接
python -c "
import pymysql;
import os;
from dotenv import load_dotenv;
load_dotenv();
try:
    conn = pymysql.connect(host='localhost', user='root', password=os.getenv('DB_PASSWORD'), database='lifemaster');
    print('✅ 数据库连接成功！');
    conn.close()
except Exception as e:
    print(f'❌ 连接失败: {e}')
"
```

## 🔧 Flask 数据库初始化

### 1. 初始化数据库迁移
```bash
# 初始化迁移仓库
flask db init

# 创建迁移文件
flask db migrate -m "Initial migration"

# 应用迁移到数据库
flask db upgrade
```

### 2. 创建数据表
```bash
# 在Python终端中直接创建表
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('数据表创建成功！')"
```

### 3. 创建管理员用户（可选）
```bash
# 创建管理员账号
python -c "
from app import app, db, User, AccountingCategory;
from werkzeug.security import generate_password_hash;
app.app_context().push();
user = User(username='admin', email='admin@lifemaster.com', password_hash=generate_password_hash('admin123'));
db.session.add(user);
db.session.commit();
print('管理员用户创建成功！用户名:admin 密码:admin123')
"
```

## 🚀 启动应用

### 1. 启动后端
```bash
python app.py
```
访问：http://localhost:5000

### 2. 启动前端
```bash
cd 前端
python -m http.server 8080
```
访问：http://localhost:8080/sign_in.html

### 3. 一键启动 (推荐)
```bash
# 生成独立的可执行文件
双击 生成exe.bat
```

## 🧪 测试验证

### 登录测试
- **用户名:** admin
- **邮箱:** admin@lifemaster.com  
- **密码:** admin123

### API 测试
```bash
# 测试登录接口
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@lifemaster.com","password":"admin123"}'
```

### 用户数据隔离测试
```bash
# 测试不同用户的数据是否独立
python test/test_user_isolation.py
```

**测试内容：**
- ✅ 不同用户的待办事项独立
- ✅ 不同用户的记账记录独立  
- ✅ 不同用户的手账独立
- ✅ 用户只能看到自己的数据

## ❗ 常见问题

### 问题1：数据库连接失败
```bash
# 解决方案
1. 检查 MySQL 服务：net start mysql
2. 验证密码：mysql -u root -p
3. 检查 .env 配置
```

### 问题2：模块导入失败
```bash
# 解决方案
pip install flask flask-sqlalchemy pymysql
```

### 问题3：数据库重置
```bash
# 重新创建所有表（会删除所有数据）
python -c "from app import app, db; app.app_context().push(); db.drop_all(); db.create_all(); print('数据库重置完成！')"
```

## 📁 相关文件

- `app.py` - Flask 主应用
- `.env` - 环境配置文件
- `生成exe.bat` - 生成可执行文件脚本

## ✅ 完成标志

当你看到以下输出时，说明配置成功：

```
✅ 数据库连接成功！
✅ 数据库表创建成功
✅ 管理员用户创建成功
 * Running on http://127.0.0.1:5000
```

现在可以开始使用 LifeMaster 了！🎉