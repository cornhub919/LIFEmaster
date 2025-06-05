#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LifeMaster 项目快速启动脚本
用于快速设置和启动项目
"""

import os
import sys
import subprocess
from pathlib import Path
import requests
import json

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}...")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"✅ {description} 成功完成")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"错误: {e.stderr}")
        return False

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {description} 已存在")
        return True
    else:
        print(f"❌ {description} 不存在")
        return False

def create_env_file():
    """创建示例 .env 文件"""
    env_content = """# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=lifemaster

# JWT 配置
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-in-production

# Flask 配置
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ 已创建示例 .env 文件")
    print("⚠️  请修改 .env 文件中的数据库密码和 JWT 密钥")

def quick_start_test():
    """
    LifeMaster 快速启动测试
    自动测试所有核心功能是否正常工作
    """
    
    print("🚀 LifeMaster 快速启动测试")
    print("=" * 50)
    
    base_url = 'http://localhost:5000'
    
    # 测试服务器连接
    print("1. 测试服务器连接...")
    try:
        response = requests.get(f'{base_url}/')
        print("✅ 服务器连接正常")
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        print("请确保后端服务正在运行: python app.py")
        return False
    
    # 测试用户注册
    print("\n2. 测试用户注册...")
    register_data = {
        "username": "quicktest",
        "email": "quicktest@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f'{base_url}/api/auth/register', 
                               json=register_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            print("✅ 用户注册成功")
        elif response.status_code == 400 and "已存在" in response.text:
            print("ℹ️ 用户已存在，继续测试")
        else:
            print(f"⚠️ 注册响应: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 注册测试失败: {e}")
        return False
    
    # 测试用户登录
    print("\n3. 测试用户登录...")
    login_data = {
        "email": "quicktest@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f'{base_url}/api/auth/login',
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result['data']['token']
            print("✅ 用户登录成功")
            print(f"   用户名: {login_result['data']['user']['username']}")
            print(f"   Token: {token[:20]}...")
            
            # 测试需要认证的API
            headers = {'Authorization': f'Bearer {token}'}
            
            # 测试获取任务列表
            print("\n4. 测试待办事项API...")
            tasks_response = requests.get(f'{base_url}/api/tasks', headers=headers)
            if tasks_response.status_code == 200:
                print("✅ 待办事项API正常")
            else:
                print(f"⚠️ 待办事项API异常: {tasks_response.status_code}")
            
            # 测试获取记账分类
            print("\n5. 测试记账API...")
            categories_response = requests.get(f'{base_url}/api/accounting/categories', headers=headers)
            if categories_response.status_code == 200:
                print("✅ 记账API正常")
                categories = categories_response.json()
                print(f"   默认分类数量: {len(categories['data']['income']) + len(categories['data']['expense'])}")
            else:
                print(f"⚠️ 记账API异常: {categories_response.status_code}")
            
            # 测试获取手账列表
            print("\n6. 测试手账API...")
            handbooks_response = requests.get(f'{base_url}/api/handbooks', headers=headers)
            if handbooks_response.status_code == 200:
                print("✅ 手账API正常")
            else:
                print(f"⚠️ 手账API异常: {handbooks_response.status_code}")
                
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 LifeMaster 快速启动测试完成！")
    print("所有核心功能正常工作，可以开始使用了！")
    
    print("\n📋 下一步操作：")
    print("1. 打开浏览器访问: 前端/sign_in.html")
    print("2. 注册新账号或使用测试账号登录")
    print("3. 体验各个功能模块")
    
    return True

def show_system_status():
    """显示系统状态信息"""
    print("\n📊 系统状态信息：")
    print(f"Python版本: {sys.version}")
    
    # 检查必要的包
    required_packages = ['requests', 'flask', 'flask_sqlalchemy', 'flask_jwt_extended']
    for package in required_packages:
        try:
            __import__(package.replace('_', '.'))
            print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")

def main():
    """主函数"""
    print("🚀 LifeMaster 项目快速启动")
    print("=" * 50)
    
    # 检查当前目录
    if not Path('app.py').exists():
        print("❌ 请在项目根目录下运行此脚本")
        sys.exit(1)
    
    # 1. 检查 .env 文件
    print("\n📋 步骤 1: 检查环境配置")
    if not check_file_exists('.env', '.env 配置文件'):
        create_env = input("是否创建示例 .env 文件? (y/n): ")
        if create_env.lower() == 'y':
            create_env_file()
        else:
            print("❌ 请手动创建 .env 文件")
            return
    
    # 2. 安装依赖
    print("\n📦 步骤 2: 安装项目依赖")
    install_deps = input("是否安装项目依赖? (y/n): ")
    if install_deps.lower() == 'y':
        if not run_command("pip install -r requirements.txt", "安装项目依赖"):
            print("❌ 依赖安装失败，请手动安装")
            return
    
    # 3. 测试数据库连接
    print("\n🔗 步骤 3: 测试数据库连接")
    test_db = input("是否测试数据库连接? (y/n): ")
    if test_db.lower() == 'y':
        if not run_command("python test_db_connection.py", "测试数据库连接"):
            print("❌ 数据库连接失败，请检查配置")
            return
    
    # 4. 初始化数据库
    print("\n🗄️  步骤 4: 初始化数据库")
    init_db = input("是否初始化数据库? (y/n): ")
    if init_db.lower() == 'y':
        # 检查是否已经初始化过
        if Path('migrations').exists():
            print("⚠️  数据库迁移文件夹已存在，跳过 flask db init")
        else:
            if not run_command("flask db init", "初始化数据库迁移"):
                print("❌ 数据库初始化失败")
                return
        
        # 创建迁移文件
        if not run_command("flask db migrate -m 'Initial migration'", "创建数据库迁移文件"):
            print("❌ 创建迁移文件失败")
            return
        
        # 应用迁移
        if not run_command("flask db upgrade", "应用数据库迁移"):
            print("❌ 应用迁移失败")
            return
    
    # 5. 启动应用
    print("\n🎉 设置完成!")
    print("\n可用的命令:")
    print("  python app.py                    # 启动开发服务器")
    print("  python test_db_connection.py     # 测试数据库连接")
    print("  flask db migrate -m 'message'    # 创建新的迁移文件")
    print("  flask db upgrade                 # 应用迁移到数据库")
    print("  flask db downgrade               # 回滚数据库迁移")
    
    start_app = input("\n是否立即启动应用? (y/n): ")
    if start_app.lower() == 'y':
        print("\n🚀 启动 LifeMaster 应用...")
        print("访问地址: http://localhost:5000")
        print("按 Ctrl+C 停止服务器")
        os.system("python app.py")

    print("请选择操作：")
    print("1. 运行完整测试")
    print("2. 查看系统状态")
    print("3. 退出")
    
    choice = input("\n请输入选项 (1-3): ").strip()
    
    if choice == '1':
        quick_start_test()
    elif choice == '2':
        show_system_status()
    elif choice == '3':
        print("再见！")
    else:
        print("无效选项")

if __name__ == "__main__":
    main()