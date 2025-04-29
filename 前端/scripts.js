// API 基础配置
const API_BASE_URL = 'http://localhost:5000';
let jwtToken = localStorage.getItem('jwt_token'); // 从本地存储获取 JWT Token

// 获取元素
const registerBtn = document.querySelector('.register-btn');
const modal = document.getElementById('register-modal');
const closeBtn = document.querySelector('.close-btn');

// 点击注册按钮显示弹窗
registerBtn.addEventListener('click', () => {
    modal.style.display = 'flex'; // 显示弹窗
});


// 点击关闭按钮隐藏弹窗
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none'; // 隐藏弹窗
});

// 点击弹窗外部隐藏弹窗
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none'; // 隐藏弹窗
    }
});

// 获取元素
const loginBtn = document.querySelector('.login-btn');
const modal2 = document.getElementById('login-modal');
const closeBtn2 = document.querySelector('.close-btn2'); // 获取第二个关闭按钮
const submitBtn = document.querySelector('.submit-btn'); // 提交按钮

// 点击注册按钮显示弹窗
loginBtn.addEventListener('click', () => {
    modal2.style.display = 'flex'; // 显示弹窗
});

// 点击关闭按钮隐藏弹窗
closeBtn2.addEventListener('click', () => {
    modal2.style.display = 'none'; // 隐藏弹窗
});

// 点击弹窗外部隐藏弹窗
window.addEventListener('click', (event) => {
    if (event.target === modal2) {
        modal2.style.display = 'none'; // 隐藏弹窗
    }
});

// 获取注册和登录弹窗相关的元素
const registerModal = document.getElementById('register-modal');
const loginModal = document.getElementById('login-modal');
const registerForm = document.querySelector('#register-modal form');
const loginForm = document.querySelector('#login-modal form');

// 显示提示框函数
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message; // 设置提示内容
    toast.classList.add('show'); // 显示提示框

    // 2秒后隐藏提示框
    setTimeout(() => {
        toast.classList.remove('show'); // 隐藏提示框
    }, 2000);
}

// 注册表单提交后切换到登录弹窗
registerForm.addEventListener('submit', (event) => {
    event.preventDefault(); // 阻止默认表单提交行为
    // registerModal.style.display = 'none'; // 关闭注册弹窗
    // loginModal.style.display = 'flex'; // 显示登录弹窗
    // showToast('注册成功！'); // 显示提示框
    handleRegister(); // 调用异步处理函数
});

// 异步注册处理函数
async function handleRegister() {
    const username = registerForm.elements.username.value;
    const password = registerForm.elements.password.value;
    const confirmPassword = registerForm.elements['confirm-password'].value;
    
    // 前端验证
    if (password !== confirmPassword) {
        showToast('两次密码输入不一致', false);
        return;
    }
    
    if (username.length < 3) {
        showToast('用户名至少需要3个字符', false);
        return;
    }
    
    if (password.length < 6) {
        showToast('密码至少需要6个字符', false);
        return;
    }
    
    try {
        // 禁用按钮防止重复提交
        const submitBtn = registerForm.querySelector('.submit-btn');
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            showToast('注册成功！');
            registerModal.style.display = 'none';
            // 自动填充登录邮箱
            loginForm.elements.username.value = `${username}@example.com`;
            loginModal.style.display = 'flex';
        } else {
            showToast(result.msg || '注册失败', false);
        }
    } catch (error) {
        showToast('网络错误，请稍后重试', false);
        console.error('注册错误:', error);
    } finally {
        // 重新启用按钮
        const submitBtn = registerForm.querySelector('.submit-btn');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    }
}

// 登录表单提交后跳转到主页面
loginForm.addEventListener('submit', (event) => {
    event.preventDefault(); // 阻止默认表单提交行为
    // window.location.href = 'main.html'; // 跳转到主页面
    // showToast('登录成功！'); // 显示提示框
    handleLogin(); // 调用异步处理函数
    
});

// 异步登录处理函数
async function handleLogin() {
    const username = loginForm.elements.username.value;
    const password = loginForm.elements.password.value;
    const email = username.includes('@') ? username : `${username}@example.com`;
    
    try {
        // 禁用按钮防止重复提交
        const submitBtn = loginForm.querySelector('.submit-btn');
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');
        
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const result = await response.json();
        
        if (result.code === 0) {
            jwtToken = result.data.token;
            localStorage.setItem('jwt_token', jwtToken);
            showToast('登录成功！');
            setTimeout(() => {
                window.location.href = 'main.html';
            }, 1000);
        } else {
            showToast(result.msg || '登录失败', false);
        }
    } catch (error) {
        showToast('网络错误，请稍后重试', false);
        console.error('登录错误:', error);
    } finally {
        // 重新启用按钮
        const submitBtn = loginForm.querySelector('.submit-btn');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    }
}

// 检查登录状态
function checkLoginStatus() {
    if (jwtToken) {
        // 如果已登录，直接跳转到主页面
        window.location.href = 'main.html';
    }
}

// 页面加载时检查登录状态
window.addEventListener('DOMContentLoaded', checkLoginStatus);


