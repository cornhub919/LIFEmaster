from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv
import pymysql
import time

# 加载环境变量
load_dotenv()

# 连接到mysql数据库
engine = create_engine('mysql+pymysql://root:8zg4ln7q@dbconn.sealosqzg.site:36615/mysql?charset=utf8mb4')

try:
    with engine.connect() as conn:
        # 创建lifemaster数据库
        conn.execute(text("CREATE DATABASE IF NOT EXISTS lifemaster CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        print("数据库创建成功！")
        
        # 查看所有数据库
        result = conn.execute(text("SHOW DATABASES"))
        print("当前数据库列表：")
        for row in result:
            print(f"- {row[0]}")
            
except Exception as e:
    print(f"连接失败: {e}")

def test_sealos_connection():
    """测试Sealos数据库连接和数据读写"""
    print("🔍 开始测试Sealos数据库连接...")
    
    try:
        # 解析DATABASE_URL
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("未找到DATABASE_URL环境变量")
            
        print(f"📊 数据库连接URL: {db_url}")
        
        # 提取连接信息（格式: mysql+pymysql://user:pass@host:port/db?charset=utf8mb4)
        parts = db_url.replace('mysql+pymysql://', '').split('@')
        user_pass = parts[0].split(':')
        host_db = parts[1].split('/')
        
        user = user_pass[0]
        password = user_pass[1]
        host = host_db[0].split(':')[0]
        port = int(host_db[0].split(':')[1])
        db_name = host_db[1].split('?')[0]
        
        print(f"📋 连接信息:\n  - 主机: {host}\n  - 端口: {port}\n  - 用户: {user}\n  - 数据库: {db_name}")
        
        # 连接数据库
        print("🔌 连接到数据库...")
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            charset='utf8mb4'
        )
        
        print("✅ 连接成功!")
        
        # 创建游标
        cursor = conn.cursor()
        
        # 查看数据库中的表
        print("📊 查询数据库表...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"📋 数据库中的表 ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
                
            # 查看users表结构
            try:
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                print("\n📋 users表结构:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            except Exception as e:
                print(f"❌ 查询users表结构失败: {e}")
                
            # 查看用户数量
            try:
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                print(f"\n👥 当前用户数量: {user_count}")
            except Exception as e:
                print(f"❌ 查询用户数量失败: {e}")
        else:
            print("⚠️ 数据库中没有表，可能需要初始化数据库")
        
        # 写入测试数据
        try:
            test_table = f"test_table_{int(time.time())}"
            print(f"\n📝 创建测试表 {test_table}...")
            
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {test_table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 插入测试数据
            print("📝 插入测试数据...")
            cursor.execute(f"INSERT INTO {test_table} (name) VALUES ('测试数据')")
            conn.commit()
            
            # 查询测试数据
            cursor.execute(f"SELECT * FROM {test_table}")
            test_data = cursor.fetchall()
            print(f"📋 测试数据: {test_data}")
            
            # 删除测试表
            print(f"🗑️ 删除测试表 {test_table}...")
            cursor.execute(f"DROP TABLE {test_table}")
            conn.commit()
            
            print("✅ 测试完成: 写入和读取数据成功!")
            
        except Exception as e:
            print(f"❌ 测试数据操作失败: {e}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sealos_connection()
    if success:
        print("\n✅✅✅ 测试成功: Sealos数据库连接和操作正常! ✅✅✅")
        sys.exit(0)
    else:
        print("\n❌❌❌ 测试失败: Sealos数据库连接或操作异常! ❌❌❌")
        sys.exit(1)
