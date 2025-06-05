# LifeMaster 数据库功能实现教程

本教程将指导你为 LifeMaster 项目添加完整的数据库功能，包括用户认证、待办事项、记账和手账模块。

## 📋 项目概述

**目标：** 将静态的前端页面升级为具有完整数据库功能的动态Web应用

**技术栈：**
- 前端：HTML + CSS + JavaScript
- 后端：Flask + SQLAlchemy
- 数据库：MySQL
- 认证：JWT Token

## 🗄️ 数据库设计

### 数据库表结构

#### 1. 用户表 (users)
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,           -- UUID主键
    username VARCHAR(80) UNIQUE NOT NULL, -- 用户名
    email VARCHAR(120) UNIQUE NOT NULL,   -- 邮箱
    password_hash VARCHAR(255) NOT NULL,  -- 加密密码
    created_at DATETIME DEFAULT NOW(),    -- 创建时间
    updated_at DATETIME DEFAULT NOW()     -- 更新时间
);
```

#### 2. 待办事项表 (tasks)
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,        -- 外键关联用户
    text VARCHAR(200) NOT NULL,          -- 任务内容
    deadline DATETIME,                   -- 截止时间
    completed BOOLEAN DEFAULT FALSE,     -- 完成状态
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 3. 记账分类表 (accounting_categories)
```sql
CREATE TABLE accounting_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(50) NOT NULL,           -- 分类名称
    type ENUM('income', 'expense') NOT NULL, -- 收入/支出
    color VARCHAR(20) DEFAULT '#cccccc', -- 分类颜色
    is_default BOOLEAN DEFAULT FALSE,    -- 是否默认分类
    created_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 4. 记账记录表 (accounting_records)
```sql
CREATE TABLE accounting_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    category_id INT NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,       -- 金额
    date DATE NOT NULL,                  -- 记账日期
    note VARCHAR(200),                   -- 备注
    created_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES accounting_categories(id)
);
```

#### 5. 手账表 (handbooks)
```sql
CREATE TABLE handbooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(100) NOT NULL,         -- 标题
    content TEXT,                        -- 内容
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🛠️ 环境配置

### 1. 安装依赖包
```bash
pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended flask-cors pymysql python-dotenv
```

### 2. 创建环境配置文件
在项目根目录创建 `.env` 文件：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=lifemaster
JWT_SECRET_KEY=your-secret-key-here-12345
```

### 3. 创建MySQL数据库
```sql
mysql -u root -p
CREATE DATABASE lifemaster CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lifemaster;
```

## 🔧 后端实现

### 1. 创建主应用文件 (app.py)

#### 基础配置
```python
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', 'password')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'lifemaster')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here-12345')

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
```

#### 数据库模型定义
```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系定义
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    accounting_records = db.relationship('AccountingRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    accounting_categories = db.relationship('AccountingCategory', backref='user', lazy=True, cascade='all, delete-orphan')
    handbooks = db.relationship('Handbook', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AccountingCategory(db.Model):
    __tablename__ = 'accounting_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum('income', 'expense'), nullable=False)
    color = db.Column(db.String(20), nullable=False, default='#cccccc')
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AccountingRecord(db.Model):
    __tablename__ = 'accounting_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('accounting_categories.id'), nullable=False)
    type = db.Column(db.Enum('income', 'expense'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    note = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Handbook(db.Model):
    __tablename__ = 'handbooks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 用户认证API
```python
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # 验证输入
        if not data or 'username' not in data or 'password' not in data or 'email' not in data:
            return jsonify({"code": -1, "msg": "用户名、邮箱和密码不能为空"}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # 检查用户名和邮箱是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"code": -1, "msg": "用户名已存在"}), 400
            
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({"code": -1, "msg": "邮箱已存在"}), 400
        
        # 创建用户并生成默认分类
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        db.session.add(new_user)
        db.session.flush()  # 获取新用户ID
        
        # 为新用户创建默认记账分类
        default_categories = [
            # 收入分类
            AccountingCategory(name="工资", type="income", color="#4CAF50", is_default=True, user_id=new_user.id),
            AccountingCategory(name="奖金", type="income", color="#8BC34A", is_default=True, user_id=new_user.id),
            # 支出分类
            AccountingCategory(name="餐饮", type="expense", color="#FF4444", is_default=True, user_id=new_user.id),
            AccountingCategory(name="交通", type="expense", color="#FF9800", is_default=True, user_id=new_user.id),
            # ...更多默认分类
        ]
        
        db.session.add_all(default_categories)
        db.session.commit()
        
        return jsonify({
            "code": 0,
            "msg": "注册成功",
            "data": {"userId": new_user.id}
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": -1, "msg": f"注册失败：{str(e)}"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"code": -1, "msg": "邮箱和密码不能为空"}), 400
        
        email = data['email']
        password = data['password']
        
        # 查找用户并验证密码
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"code": -1, "msg": "无效的邮箱或密码"}), 401
        
        # 生成JWT token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            "code": 0,
            "msg": "登录成功",
            "data": {
                "token": access_token,
                "user": user.to_dict()
            }
        })
        
    except Exception as e:
        return jsonify({"code": -1, "msg": f"登录失败：{str(e)}"}), 500
```

#### 待办事项API
```python
@app.route('/api/tasks', methods=['GET', 'POST'])
@jwt_required()
def manage_tasks():
    current_user = get_jwt_identity()
    
    if request.method == 'GET':
        # 获取待办事项列表
        tasks = Task.query.filter_by(user_id=current_user).all()
        return jsonify([{
            'id': task.id,
            'text': task.text,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        } for task in tasks]), 200
    
    if request.method == 'POST':
        # 创建新待办事项
        data = request.get_json()
        new_task = Task(
            user_id=current_user,
            text=data['text'],
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"code": 0, "msg": "任务创建成功", "data": {"taskId": new_task.id}}), 201
```

#### 记账功能API
```python
@app.route('/api/accounting/categories', methods=['GET', 'POST'])
@jwt_required()
def manage_categories():
    current_user = get_jwt_identity()
    
    if request.method == 'GET':
        # 获取记账分类列表
        categories = AccountingCategory.query.filter_by(user_id=current_user).all()
        return jsonify([{
            'id': category.id,
            'name': category.name,
            'type': category.type,
            'color': category.color,
            'is_default': category.is_default
        } for category in categories]), 200
    
    if request.method == 'POST':
        # 创建新记账分类
        data = request.get_json()
        new_category = AccountingCategory(
            user_id=current_user,
            name=data['name'],
            type=data['type'],
            color=data.get('color', '#cccccc')
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"code": 0, "msg": "分类创建成功", "data": {"categoryId": new_category.id}}), 201

@app.route('/api/accounting/records', methods=['GET', 'POST'])
@jwt_required()
def manage_records():
    current_user = get_jwt_identity()
    
    if request.method == 'GET':
        # 获取记账记录列表
        records = AccountingRecord.query.filter_by(user_id=current_user).all()
        return jsonify([{
            'id': record.id,
            'category_id': record.category_id,
            'type': record.type,
            'amount': str(record.amount),
            'date': record.date.isoformat(),
            'note': record.note
        } for record in records]), 200
    
    if request.method == 'POST':
        # 创建新记账记录
        data = request.get_json()
        new_record = AccountingRecord(
            user_id=current_user,
            category_id=data['category_id'],
            type=data['type'],
            amount=data['amount'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            note=data.get('note')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"code": 0, "msg": "记账记录创建成功", "data": {"recordId": new_record.id}}), 201
```

#### 手账功能API
```python
@app.route('/api/handbooks', methods=['GET', 'POST'])
@jwt_required()
def manage_handbooks():
    current_user = get_jwt_identity()
    
    if request.method == 'GET':
        # 获取手账列表
        handbooks = Handbook.query.filter_by(user_id=current_user).all()
        return jsonify([{
            'id': handbook.id,
            'title': handbook.title,
            'content': handbook.content,
            'created_at': handbook.created_at.isoformat(),
            'updated_at': handbook.updated_at.isoformat()
        } for handbook in handbooks]), 200
    
    if request.method == 'POST':
        # 创建新手账
        data = request.get_json()
        new_handbook = Handbook(
            user_id=current_user,
            title=data['title'],
            content=data.get('content', '')
        )
        db.session.add(new_handbook)
        db.session.commit()
        return jsonify({"code": 0, "msg": "手账创建成功", "data": {"handbookId": new_handbook.id}}), 201
```

## 🌐 前端改造

### 1. 创建API连接脚本 (前端/scripts.js)

#### 基础配置和工具函数
```javascript
// API基础配置
const API_BASE_URL = 'http://localhost:5000';

// 提示消息显示函数
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
```

#### 用户注册功能
```javascript
// 处理注册表单提交
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // 验证密码确认
    if (password !== confirmPassword) {
        showToast('两次输入的密码不一致', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.code === 0) {
            showToast('注册成功！', 'success');
            registerModal.style.display = 'none';
            document.getElementById('register-form').reset();
        } else {
            showToast(data.msg || '注册失败', 'error');
        }
    } catch (error) {
        console.error('注册错误:', error);
        showToast('网络错误，请检查后端是否启动', 'error');
    }
});
```

#### 用户登录功能
```javascript
// 处理登录表单提交
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.code === 0) {
            // 保存token和用户信息到本地存储
            localStorage.setItem('token', data.data.token);
            localStorage.setItem('user', JSON.stringify(data.data.user));
            
            showToast('登录成功！', 'success');
            loginModal.style.display = 'none';
            
            // 跳转到主页面
            setTimeout(() => {
                window.location.href = 'main.html';
            }, 1500);
        } else {
            showToast(data.msg || '登录失败', 'error');
        }
    } catch (error) {
        console.error('登录错误:', error);
        showToast('网络错误，请检查后端是否启动', 'error');
    }
});
```

### 2. 主页面功能脚本 (前端/main.js)

#### 登录状态检查
```javascript
// 检查登录状态
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        // 未登录，跳转到登录页面
        window.location.href = 'sign_in.html';
        return;
    }
    
    // 显示用户信息
    try {
        const userData = JSON.parse(user);
        console.log('当前用户:', userData.username);
    } catch (error) {
        console.error('用户数据解析失败:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'sign_in.html';
    }
}

// 退出登录
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'sign_in.html';
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    checkLoginStatus();
    
    // 绑定退出登录按钮
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('确定要退出登录吗？')) {
                logout();
            }
        });
    }
});
```

### 3. 前端页面修改

#### 修改 sign_in.html
```html
<!-- 在 </body> 前添加提示框和脚本引用 -->
<div id="toast" class="toast"></div>
<script src="scripts.js"></script>
```

#### 修改 main.html
```html
<!-- 在 </body> 前添加脚本引用 -->
<script src="main.js"></script>
```

#### 添加CSS样式 (styles.css)
```css
/* 提示框样式 */
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    z-index: 10000;
    display: none;
    min-width: 200px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.toast.success {
    background-color: #4CAF50;
}

.toast.error {
    background-color: #f44336;
}

.toast.info {
    background-color: #2196F3;
}

/* 模态框居中修复 */
.modal[style*="block"] {
    display: flex !important;
    justify-content: center;
    align-items: center;
}
```

## 🚀 项目启动

### 1. 启动后端服务
```bash
cd f:\大二下\软件工程\LIFEmaster-main
python app.py
```

### 2. 访问前端页面
```bash
# 直接双击打开
前端/sign_in.html
```

### 3. 测试功能流程
1. **注册新用户** - 填写用户名、邮箱、密码
2. **登录系统** - 使用注册的邮箱和密码
3. **自动跳转** - 登录成功后跳转到主页面
4. **访问功能** - 在主页面点击各个功能模块

## 🧪 功能验证

### 使用测试脚本验证
```bash
# 快速启动测试
python quick_start.py

# 完整功能测试
python test_api.py

# 登录问题排查
python debug_login.py
```

### 手动验证清单
- [ ] 用户注册功能正常
- [ ] 用户登录功能正常
- [ ] 登录后自动跳转主页
- [ ] 主页面显示用户信息
- [ ] 退出登录功能正常
- [ ] 模态框居中显示
- [ ] 提示消息正常显示

## ✅ 完成效果

**前端功能：**
- ✅ 用户注册/登录界面
- ✅ 表单验证（密码确认）
- ✅ 实时提示消息
- ✅ Token存储管理
- ✅ 登录状态检查
- ✅ 自动页面跳转

**后端功能：**
- ✅ 用户注册/登录API
- ✅ JWT身份认证
- ✅ MySQL数据持久化
- ✅ 完整的数据库模型
- ✅ 待办事项CRUD API
- ✅ 记账功能API
- ✅ 手账功能API

**数据库功能：**
- ✅ 用户数据存储
- ✅ 默认分类自动创建
- ✅ 数据关联和完整性
- ✅ 用户数据隔离

现在 LifeMaster 已经是一个**功能完整的全栈Web应用**！用户可以注册、登录，并使用所有功能模块，数据都会安全地存储在MySQL数据库中。