# LifeMaster 测试程序使用说明

本目录包含三个主要测试脚本：

- `test_api.py`：API功能全流程测试（注册、登录、任务、记账、手账等）
- `test_db_connection.py`：数据库连接测试
- `test_user_isolation.py`：用户数据隔离性测试

## 运行方法

1. **确保后端服务已启动**
   ```bash
   python app.py
   ```
   看到 `Running on http://127.0.0.1:5000/` 表示启动成功。

2. **运行API功能测试**
   ```bash
   python test/test_api.py
   ```
   按提示选择测试模式，推荐选择 2 进行完整功能测试。

3. **运行数据库连接测试**
   ```bash
   python test/test_db_connection.py
   ```
   能看到“数据库连接成功”即为正常。

4. **运行用户隔离性测试**
   ```bash
   python test/test_user_isolation.py
   ```
   能看到“不同用户的数据互不干扰”即为正常。

## 常见问题

- 如果提示“服务器连接失败”，请先启动后端服务。
- 如果注册时提示“用户名已存在”，说明该测试用户已注册过，直接用其登录即可。
- 如需清空数据库，请手动删除数据库数据或重建数据库。

## 说明


- 测试脚本默认连接 `http://localhost:5000`，如有端口变动请在脚本内修改 `base_url`。

---
如有其它测试需求，可在本目录下新增脚本。
