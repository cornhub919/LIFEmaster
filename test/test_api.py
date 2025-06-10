import requests
import json
from datetime import datetime, date

class LifeMasterAPITester:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        
    def test_user_auth(self):
        """测试用户认证功能"""
        print("🔐 测试用户认证功能")
        print("-" * 30)
        
        # 测试注册
        register_data = {
            "username": "apitester",
            "email": "apitester@test.com",
            "password": "test123456"
        }
        
        print("1. 测试用户注册...")
        response = requests.post(f'{self.base_url}/api/auth/register', 
                               json=register_data)
        
        if response.status_code == 201:
            print("✅ 注册成功")
        elif "已存在" in response.text:
            print("ℹ️ 用户已存在，继续测试")
        else:
            print(f"⚠️ 注册异常: {response.text}")
        
        # 测试登录
        print("2. 测试用户登录...")
        login_data = {
            "email": "apitester@test.com",
            "password": "test123456"
        }
        
        response = requests.post(f'{self.base_url}/api/auth/login', 
                               json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['data']['token']
            self.user_id = result['data']['user']['id']
            print("✅ 登录成功")
            print(f"   用户ID: {self.user_id}")
            return True
        else:
            print(f"❌ 登录失败: {response.text}")
            return False
    
    def get_headers(self):
        """获取认证头"""
        return {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
    
    def test_tasks_api(self):
        """测试待办事项API"""
        print("\n📝 测试待办事项API")
        print("-" * 30)
        
        headers = self.get_headers()
        
        # 创建任务
        print("1. 创建新任务...")
        task_data = {
            "text": "API测试任务",
            "deadline": "2024-12-31T23:59:59",
            "completed": False
        }
        
        response = requests.post(f'{self.base_url}/api/tasks', 
                               json=task_data, headers=headers)
        
        if response.status_code == 201:
            task = response.json()['data']
            task_id = task['id']
            print("✅ 任务创建成功")
            print(f"   任务ID: {task_id}")
            
            # 获取任务列表
            print("2. 获取任务列表...")
            response = requests.get(f'{self.base_url}/api/tasks', headers=headers)
            if response.status_code == 200:
                tasks = response.json()['data']['tasks']
                print(f"✅ 获取到 {len(tasks)} 个任务")
            
            # 更新任务
            print("3. 更新任务状态...")
            update_data = {"completed": True}
            response = requests.put(f'{self.base_url}/api/tasks/{task_id}', 
                                  json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ 任务更新成功")
            
            # 删除任务
            print("4. 删除测试任务...")
            response = requests.delete(f'{self.base_url}/api/tasks/{task_id}', 
                                     headers=headers)
            if response.status_code == 200:
                print("✅ 任务删除成功")
            
        else:
            print(f"❌ 创建任务失败: {response.text}")
    
    def test_accounting_api(self):
        """测试记账API"""
        print("\n💰 测试记账API")
        print("-" * 30)
        
        headers = self.get_headers()
        
        # 获取分类
        print("1. 获取记账分类...")
        response = requests.get(f'{self.base_url}/api/accounting/categories', 
                              headers=headers)
        
        if response.status_code == 200:
            categories = response.json()['data']
            print(f"✅ 获取分类成功")
            print(f"   收入分类: {len(categories['income'])} 个")
            print(f"   支出分类: {len(categories['expense'])} 个")
            
            # 使用第一个支出分类创建记录
            if categories['expense']:
                category_id = categories['expense'][0]['id']
                
                print("2. 创建记账记录...")
                record_data = {
                    "type": "expense",
                    "category_id": category_id,
                    "amount": 50.00,
                    "date": date.today().isoformat(),
                    "note": "API测试记录"
                }
                
                response = requests.post(f'{self.base_url}/api/accounting/records', 
                                       json=record_data, headers=headers)
                
                if response.status_code == 201:
                    print("✅ 记账记录创建成功")
                    
                    # 获取记录列表
                    print("3. 获取记账记录...")
                    response = requests.get(f'{self.base_url}/api/accounting/records', 
                                          headers=headers)
                    if response.status_code == 200:
                        records = response.json()['data']['records']
                        print(f"✅ 获取到 {len(records)} 条记录")
        
        else:
            print(f"❌ 获取分类失败: {response.text}")
    
    def test_handbook_api(self):
        """测试手账API"""
        print("\n📖 测试手账API")
        print("-" * 30)
        
        headers = self.get_headers()
        
        # 创建手账
        print("1. 创建新手账...")
        handbook_data = {
            "title": "API测试手账",
            "content": "这是一个API测试创建的手账内容。\n\n包含多行文本。"
        }
        
        response = requests.post(f'{self.base_url}/api/handbooks', 
                               json=handbook_data, headers=headers)
        
        if response.status_code == 201:
            handbook = response.json()['data']
            handbook_id = handbook['id']
            print("✅ 手账创建成功")
            print(f"   手账ID: {handbook_id}")
            
            # 获取手账列表
            print("2. 获取手账列表...")
            response = requests.get(f'{self.base_url}/api/handbooks', headers=headers)
            if response.status_code == 200:
                handbooks = response.json()['data']['handbooks']
                print(f"✅ 获取到 {len(handbooks)} 个手账")
            
            # 获取单个手账
            print("3. 获取手账详情...")
            response = requests.get(f'{self.base_url}/api/handbooks/{handbook_id}', 
                                  headers=headers)
            if response.status_code == 200:
                print("✅ 获取手账详情成功")
            
            # 更新手账
            print("4. 更新手账内容...")
            update_data = {
                "title": "API测试手账（已更新）",
                "content": "更新后的手账内容"
            }
            response = requests.put(f'{self.base_url}/api/handbooks/{handbook_id}', 
                                  json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ 手账更新成功")
            
            # 删除手账
            print("5. 删除测试手账...")
            response = requests.delete(f'{self.base_url}/api/handbooks/{handbook_id}', 
                                     headers=headers)
            if response.status_code == 200:
                print("✅ 手账删除成功")
        
        else:
            print(f"❌ 创建手账失败: {response.text}")
    
    def run_complete_test(self):
        """运行完整的API测试"""
        print("🧪 LifeMaster API 完整测试")
        print("=" * 50)
        
        # 测试认证
        if not self.test_user_auth():
            print("❌ 认证测试失败，停止后续测试")
            return
        
        # 测试各个模块
        self.test_tasks_api()
        self.test_accounting_api()
        self.test_handbook_api()
        
        print("\n" + "=" * 50)
        print("🎉 API测试完成！")
        print("所有功能API都工作正常！")

def main():
    print("选择测试模式：")
    print("1. 快速连接测试")
    print("2. 完整功能测试")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    tester = LifeMasterAPITester()
    
    if choice == '1':
        try:
            response = requests.get('http://localhost:5000/')
            print("✅ 服务器连接正常")
        except:
            print("❌ 服务器连接失败，请确保后端正在运行")
    
    elif choice == '2':
        tester.run_complete_test()
    
    elif choice == '3':
        print("退出测试")
    
    else:
        print("无效选择")

if __name__ == '__main__':
    main()