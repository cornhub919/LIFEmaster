#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户数据隔离测试脚本
验证不同用户的数据是否独立
"""

import requests
import json

class UserIsolationTester:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        
    def test_user_isolation(self):
        """测试用户数据隔离"""
        print("🔒 测试用户数据隔离")
        print("=" * 50)
        
        # 创建两个测试用户
        users = [
            {
                "username": "testuser1",
                "email": "test1@example.com", 
                "password": "test123456"
            },
            {
                "username": "testuser2",
                "email": "test2@example.com",
                "password": "test123456"
            }
        ]
        
        user_tokens = []
        
        # 注册并登录两个用户
        for i, user in enumerate(users, 1):
            print(f"\n👤 处理用户 {i}: {user['username']}")
            
            # 注册用户
            print("   📝 注册用户...")
            register_response = requests.post(
                f'{self.base_url}/api/auth/register',
                json=user
            )
            
            if register_response.status_code == 201:
                print("   ✅ 注册成功")
            elif "已存在" in register_response.text:
                print("   ℹ️  用户已存在，继续测试")
            else:
                print(f"   ⚠️  注册异常: {register_response.text}")
            
            # 登录用户
            print("   🔑 登录用户...")
            login_response = requests.post(
                f'{self.base_url}/api/auth/login',
                json={"email": user['email'], "password": user['password']}
            )
            
            if login_response.status_code == 200:
                token = login_response.json()['data']['token']
                user_id = login_response.json()['data']['user']['id']
                user_tokens.append({
                    'username': user['username'],
                    'token': token,
                    'user_id': user_id,
                    'headers': {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
                })
                print(f"   ✅ 登录成功，用户ID: {user_id}")
            else:
                print(f"   ❌ 登录失败: {login_response.text}")
                return False
        
        if len(user_tokens) != 2:
            print("❌ 用户准备失败")
            return False
        
        # 测试任务数据隔离
        print(f"\n📝 测试任务数据隔离")
        self.test_tasks_isolation(user_tokens)
        
        # 测试记账数据隔离
        print(f"\n💰 测试记账数据隔离")
        self.test_accounting_isolation(user_tokens)
        
        # 测试手账数据隔离
        print(f"\n📖 测试手账数据隔离")
        self.test_handbook_isolation(user_tokens)
        
        print(f"\n🎉 用户数据隔离测试完成！")
    
    def test_tasks_isolation(self, user_tokens):
        """测试任务数据隔离"""
        
        # 用户1创建任务
        task_data = {"text": f"用户1的任务", "completed": False}
        response1 = requests.post(
            f'{self.base_url}/api/tasks',
            json=task_data,
            headers=user_tokens[0]['headers']
        )
        
        if response1.status_code == 201:
            print(f"   ✅ {user_tokens[0]['username']} 创建任务成功")
        else:
            print(f"   ❌ {user_tokens[0]['username']} 创建任务失败")
            return
        
        # 用户2创建任务
        task_data = {"text": f"用户2的任务", "completed": False}
        response2 = requests.post(
            f'{self.base_url}/api/tasks',
            json=task_data,
            headers=user_tokens[1]['headers']
        )
        
        if response2.status_code == 201:
            print(f"   ✅ {user_tokens[1]['username']} 创建任务成功")
        else:
            print(f"   ❌ {user_tokens[1]['username']} 创建任务失败")
            return
        
        # 检查用户1只能看到自己的任务
        response1 = requests.get(
            f'{self.base_url}/api/tasks',
            headers=user_tokens[0]['headers']
        )
        
        if response1.status_code == 200:
            tasks1 = response1.json()['data']['tasks']
            user1_task_count = len(tasks1)
            print(f"   📊 {user_tokens[0]['username']} 看到 {user1_task_count} 个任务")
            
            # 检查任务内容是否只包含用户1的任务
            user1_tasks = [task for task in tasks1 if "用户1" in task['text']]
            if len(user1_tasks) > 0 and all("用户2" not in task['text'] for task in tasks1):
                print(f"   ✅ 任务数据隔离正确")
            else:
                print(f"   ❌ 任务数据隔离失败！用户1看到了其他用户的任务")
        
        # 检查用户2只能看到自己的任务
        response2 = requests.get(
            f'{self.base_url}/api/tasks',
            headers=user_tokens[1]['headers']
        )
        
        if response2.status_code == 200:
            tasks2 = response2.json()['data']['tasks']
            user2_task_count = len(tasks2)
            print(f"   📊 {user_tokens[1]['username']} 看到 {user2_task_count} 个任务")
            
            # 检查任务内容是否只包含用户2的任务
            user2_tasks = [task for task in tasks2 if "用户2" in task['text']]
            if len(user2_tasks) > 0 and all("用户1" not in task['text'] for task in tasks2):
                print(f"   ✅ 任务数据隔离正确")
            else:
                print(f"   ❌ 任务数据隔离失败！用户2看到了其他用户的任务")
    
    def test_accounting_isolation(self, user_tokens):
        """测试记账数据隔离"""
        
        # 获取用户1的分类
        response1 = requests.get(
            f'{self.base_url}/api/accounting/categories',
            headers=user_tokens[0]['headers']
        )
        
        if response1.status_code == 200:
            categories1 = response1.json()['data']
            if categories1['expense']:
                category_id = categories1['expense'][0]['id']
                
                # 用户1创建记账记录
                record_data = {
                    "type": "expense",
                    "category_id": category_id,
                    "amount": 100.0,
                    "date": "2024-01-01",
                    "note": "用户1的测试记录"
                }
                
                response = requests.post(
                    f'{self.base_url}/api/accounting/records',
                    json=record_data,
                    headers=user_tokens[0]['headers']
                )
                
                if response.status_code == 201:
                    print(f"   ✅ {user_tokens[0]['username']} 创建记账记录成功")
                else:
                    print(f"   ❌ {user_tokens[0]['username']} 创建记账记录失败")
        
        # 获取用户2的分类
        response2 = requests.get(
            f'{self.base_url}/api/accounting/categories',
            headers=user_tokens[1]['headers']
        )
        
        if response2.status_code == 200:
            categories2 = response2.json()['data']
            if categories2['expense']:
                category_id = categories2['expense'][0]['id']
                
                # 用户2创建记账记录
                record_data = {
                    "type": "expense",
                    "category_id": category_id,
                    "amount": 200.0,
                    "date": "2024-01-01",
                    "note": "用户2的测试记录"
                }
                
                response = requests.post(
                    f'{self.base_url}/api/accounting/records',
                    json=record_data,
                    headers=user_tokens[1]['headers']
                )
                
                if response.status_code == 201:
                    print(f"   ✅ {user_tokens[1]['username']} 创建记账记录成功")
                else:
                    print(f"   ❌ {user_tokens[1]['username']} 创建记账记录失败")
        
        # 检查记录隔离
        for i, user_token in enumerate(user_tokens):
            response = requests.get(
                f'{self.base_url}/api/accounting/records',
                headers=user_token['headers']
            )
            
            if response.status_code == 200:
                records = response.json()['data']['records']
                user_records = [r for r in records if f"用户{i+1}" in (r['note'] or '')]
                print(f"   📊 {user_token['username']} 看到 {len(records)} 条记录")
                
                if len(user_records) > 0 and all(f"用户{2-i}" not in (r['note'] or '') for r in records):
                    print(f"   ✅ 记账数据隔离正确")
                else:
                    print(f"   ❌ 记账数据隔离失败！")
    
    def test_handbook_isolation(self, user_tokens):
        """测试手账数据隔离"""
        
        # 用户创建手账
        for i, user_token in enumerate(user_tokens, 1):
            handbook_data = {
                "title": f"用户{i}的手账",
                "content": f"这是用户{i}的手账内容"
            }
            
            response = requests.post(
                f'{self.base_url}/api/handbooks',
                json=handbook_data,
                headers=user_token['headers']
            )
            
            if response.status_code == 201:
                print(f"   ✅ {user_token['username']} 创建手账成功")
            else:
                print(f"   ❌ {user_token['username']} 创建手账失败")
        
        # 检查手账隔离
        for i, user_token in enumerate(user_tokens, 1):
            response = requests.get(
                f'{self.base_url}/api/handbooks',
                headers=user_token['headers']
            )
            
            if response.status_code == 200:
                handbooks = response.json()['data']['handbooks']
                user_handbooks = [h for h in handbooks if f"用户{i}" in h['title']]
                print(f"   📊 {user_token['username']} 看到 {len(handbooks)} 个手账")
                
                if len(user_handbooks) > 0 and all(f"用户{2-i+1 if i==1 else 1}" not in h['title'] for h in handbooks):
                    print(f"   ✅ 手账数据隔离正确")
                else:
                    print(f"   ❌ 手账数据隔离失败！")

def main():
    print("🧪 LifeMaster 用户数据隔离测试")
    print("验证不同用户的数据是否独立")
    print()
    
    tester = UserIsolationTester()
    
    try:
        # 首先测试服务器连接
        response = requests.get('http://localhost:5000/')
        print("✅ 后端服务连接正常")
        print()
        
        # 运行隔离测试
        tester.test_user_isolation()
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        print("请确保后端服务正在运行：python app.py")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")

if __name__ == '__main__':
    main()