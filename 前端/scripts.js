// API基础配置 - 使用本地地址
const API_BASE_URL = 'http://localhost:5000';

// 提示消息显示函数
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.style.display = 'block';
        
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }
}

// 获取认证头
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// 处理页面加载完成事件
document.addEventListener('DOMContentLoaded', function() {
    // 获取模态框元素
    const registerModal = document.getElementById('register-modal');
    const loginModal = document.getElementById('login-modal');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');
    const closeBtns = document.querySelectorAll('.close-btn, .close-btn2');
    
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    
    // 处理注册表单提交
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('reg-username').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            
            // 验证输入
            if (!username || !email || !password) {
                showToast('请填写完整信息', 'error');
                return;
            }
            
            if (password !== confirmPassword) {
                showToast('两次输入的密码不一致', 'error');
                return;
            }
            
            if (password.length < 6) {
                showToast('密码长度至少6位', 'error');
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
                
                if (data.code === 0) {
                    showToast('注册成功！请登录', 'success');
                    registerModal.style.display = 'none';
                    registerForm.reset();
                    // 自动打开登录弹窗
                    setTimeout(() => {
                        loginModal.style.display = 'block';
                    }, 1000);
                } else {
                    showToast(data.msg || '注册失败', 'error');
                }
            } catch (error) {
                console.error('注册错误:', error);
                showToast('网络错误，请检查后端是否启动', 'error');
            }
        });
    }
    
    // 处理登录表单提交
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('login-email').value.trim();
            const password = document.getElementById('login-password').value;
            
            if (!email || !password) {
                showToast('请填写邮箱和密码', 'error');
                return;
            }
            
            try {
                console.log(`尝试登录: ${email}`);
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
                
                // 处理网络错误
                if (!response.ok && response.status !== 401) {
                    console.error(`登录失败: ${response.status} ${response.statusText}`);
                    showToast(`登录失败: ${response.status} ${response.statusText}`, 'error');
                    return;
                }
                
                const data = await response.json();
                
                if (data.code === 0) {
                    // 保存token和用户信息到本地存储
                    localStorage.setItem('token', data.data.token);
                    localStorage.setItem('user', JSON.stringify(data.data.user));
                    
                    showToast('登录成功！', 'success');
                    loginModal.style.display = 'none';
                    
                    // 跳转到主页面
                    setTimeout(() => {
                        window.location.href = 'main.html';
                    }, 1000);
                } else {
                    showToast(data.msg || '登录失败', 'error');
                }
            } catch (error) {
                console.error('登录错误:', error);
                showToast('网络错误，请检查后端是否启动', 'error');
            }
        });
    }

    // 显示注册弹窗
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            registerModal.style.display = 'block';
        });
    }

    // 显示登录弹窗
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            loginModal.style.display = 'block';
        });
    }

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
});


