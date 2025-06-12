from flask import Flask
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel需要的WSGI应用
def handler(environ, start_response):
    return app(environ, start_response)

# 导出应用
application = app

if __name__ == '__main__':
    app.run()
