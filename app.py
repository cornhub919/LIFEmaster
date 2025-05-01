from flask import Flask, request, jsonify
from flask_jwt_extended import ( # type: ignore
    JWTManager, create_access_token, jwt_required, get_jwt_identity,
    get_jwt, set_access_cookies, unset_jwt_cookies
)
from flask_cors import CORS  # 新增导入
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import collections
if not hasattr(collections, 'Iterable'):
    collections.Iterable = collections.abc.Iterable

app = Flask(__name__)
CORS(app)  # 添加这一行以允许跨域请求
# 配置 JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here-12345'  # 生产环境中应该使用更安全的密钥
# 配置 JWT 黑名单
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']  # 黑名单检查访问令牌

jwt = JWTManager(app)

# 模拟数据库和黑名单
users_db = {}
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

# 辅助函数
def find_user_by_username(username):
    for user_id, user in users_db.items():
        if user['username'] == username:
            return user
    return None

def find_user_by_email(email):
    for user_id, user in users_db.items():
        if user['email'] == email:
            return user
    return None

# 路由
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证输入
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"code": -1, "msg": "用户名和密码不能为空"}), 400
    
    username = data['username']
    password = data['password']
    
    # 检查用户名是否已存在
    if find_user_by_username(username):
        return jsonify({"code": -1, "msg": "用户名已存在"}), 400
    
    # 创建用户
    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)
    
    # 模拟邮箱生成 (实际应用中应该由用户提供)
    email = f"{username}@example.com"
    
    users_db[user_id] = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'password': hashed_password
    }
    
    return jsonify({
        "code": 0,
        "msg": "注册成功",
        "data": {
            "userId": user_id
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"code": -1, "msg": "邮箱和密码不能为空"}), 400
    
    email = data['email']
    password = data['password']
    
    user = find_user_by_email(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"code": -1, "msg": "无效的邮箱或密码"}), 401
    
    # 创建JWT token
    access_token = create_access_token(identity=user['user_id'])
    
    return jsonify({
        "code": 0,
        "msg": "登录成功",
        "data": {
            "token": access_token
        }
    })


@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({
        "code": 0,
        "msg": "退出成功"
    })


@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = users_db.get(current_user_id)
    
    if not user:
        return jsonify({"code": -1, "msg": "用户不存在"}), 404
    
    return jsonify({
        "code": 0,
        "data": {
            "username": user['username']
        }
    })

if __name__ == '__main__':
    app.run(debug=True)