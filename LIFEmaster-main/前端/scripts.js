// API 基础配置
const API_BASE_URL = 'http://localhost:5000';

// 显示提示信息
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// 获取模态框元素
const registerModal = document.getElementById('register-modal');
const loginModal = document.getElementById('login-modal');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');
const closeBtns = document.querySelectorAll('.close-btn, .close-btn2');

// 显示注册弹窗
registerBtn.addEventListener('click', () => {
    registerModal.style.display = 'block';
});

// 显示登录弹窗
loginBtn.addEventListener('click', () => {
    loginModal.style.display = 'block';
});

// 关闭弹窗
closeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.target.closest('.modal').style.display = 'none';
    });
});

// 点击弹窗外部关闭
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// 处理注册表单提交
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    console.log('注册数据:', { username, email, password }); // 调试信息
    
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
        console.log('注册响应:', data); // 调试信息
        
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
            // 保存token到本地存储
            localStorage.setItem('token', data.data.token);
            localStorage.setItem('user', JSON.stringify(data.data.user));
            
            showToast('登录成功！', 'success');
            loginModal.style.display = 'none';
            
            // 延迟跳转到主页面
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

// 检查是否已登录
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    if (token) {
        // TODO: 验证token是否有效
        console.log('用户已登录');
    }
}
 
// 页面加载完成后检查登录状态
document.addEventListener('DOMContentLoaded', checkLoginStatus);


