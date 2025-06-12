#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接测试脚本
用于验证 MySQL 数据库连接是否正常
"""

import pymysql
import os
from dotenv import load_dotenv

def test_database_connection():
    """测试数据库连接"""
    # 加载环境变量
    load_dotenv()
    
    # 获取数据库配置
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME', 'lifemaster'),
        'charset': 'utf8mb4'
    }
    
    print("=== 数据库连接测试 ===")
    print(f"主机: {db_config['host']}:{db_config['port']}")
    print(f"用户: {db_config['user']}")
    print(f"数据库: {db_config['database']}")
    print("-" * 30)
    
    try:
        # 尝试连接数据库
        connection = pymysql.connect(**db_config)
        
        print("✅ 数据库连接成功!")
        
        # 获取数据库版本信息
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MySQL 版本: {version[0]}")
            
            # 检查数据库是否存在
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"📂 当前数据库: {current_db[0]}")
            
            # 列出所有表（如果存在）
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"📋 现有表格 ({len(tables)}个):")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("📋 数据库中暂无表格")
        
        connection.close()
        print("✅ 数据库连接测试完成")
        return True
        
    except pymysql.Error as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查 MySQL 服务是否启动")
        print("2. 验证 .env 文件中的数据库配置")
        print("3. 确认数据库用户权限")
        print("4. 检查数据库是否已创建")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def check_environment_variables():
    """检查环境变量配置"""
    print("\n=== 环境变量检查 ===")
    
    env_vars = [
        ('DB_HOST', 'localhost'),
        ('DB_PORT', '3306'),
        ('DB_USER', 'root'),
        ('DB_PASSWORD', None),
        ('DB_NAME', 'lifemaster'),
        ('JWT_SECRET_KEY', None)
    ]
    
    all_set = True
    
    for var_name, default in env_vars:
        value = os.getenv(var_name, default)
        if value:
            if var_name in ['DB_PASSWORD', 'JWT_SECRET_KEY']:
                print(f"✅ {var_name}: {'*' * len(value)}")
            else:
                print(f"✅ {var_name}: {value}")
        else:
            print(f"❌ {var_name}: 未设置")
            all_set = False
    
    if not all_set:
        print("\n🔧 请在 .env 文件中设置缺失的环境变量")
    
    return all_set

if __name__ == "__main__":
    print("🚀 LifeMaster 数据库连接测试")
    print("=" * 50)
    
    # 检查环境变量
    env_ok = check_environment_variables()
    
    if env_ok:
        # 测试数据库连接
        db_ok = test_database_connection()
        
        if db_ok:
            print("\n🎉 所有检查通过，可以开始数据库迁移！")
            print("\n下一步操作:")
            print("1. flask db init")
            print("2. flask db migrate -m 'Initial migration'")
            print("3. flask db upgrade")
        else:
            print("\n❌ 请先解决数据库连接问题")
    else:
        print("\n❌ 请先配置环境变量")