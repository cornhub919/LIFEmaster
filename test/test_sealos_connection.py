import socket
import pymysql
import requests

def test_network_connectivity():
    """测试到Sealos的网络连通性"""
    
    # 请在这里填入你从Sealos控制台获取的最新连接信息
    SEALOS_HOST = "你的最新Sealos外网地址"  # 请替换
    SEALOS_PORT = 你的端口号  # 请替换
    
    print("🔍 测试网络连通性...")
    
    # 1. 测试基础网络连接
    try:
        print(f"📡 测试TCP连接到 {SEALOS_HOST}:{SEALOS_PORT}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((SEALOS_HOST, SEALOS_PORT))
        sock.close()
        
        if result == 0:
            print("✅ TCP连接成功")
        else:
            print(f"❌ TCP连接失败: 错误码 {result}")
            return False
            
    except Exception as e:
        print(f"❌ 网络连接测试失败: {e}")
        return False
    
    # 2. 测试MySQL连接
    try:
        print("🗄️ 测试MySQL连接...")
        connection = pymysql.connect(
            host=SEALOS_HOST,
            port=SEALOS_PORT,
            user='root',
            password='8zg4ln7q',
            connect_timeout=10,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ MySQL连接成功")
            
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("📋 可用数据库:")
        for db in databases:
            print(f"  - {db[0]}")
            
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        return False

if __name__ == "__main__":
    if test_network_connectivity():
        print("\n🎉 Sealos连接测试成功！可以使用云端数据库")
    else:
        print("\n💥 Sealos连接测试失败！请检查网络或连接信息")
