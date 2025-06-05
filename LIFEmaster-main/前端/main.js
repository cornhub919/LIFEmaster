const API_BASE_URL = 'http://localhost:5000'; // 确保在生产环境中替换为正确的地址
const jwtToken = localStorage.getItem('jwt_token'); // 从本地存储获取 JWT Token

// 检查登录状态
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    if (!token || !user) {
        // 未登录，跳转到登录页面
        window.location.href = 'sign_in.html';
        return;
    }
    
    // 显示用户信息
    try {
        const userData = JSON.parse(user);
        console.log('当前用户:', userData.username);
    } catch (error) {
        console.error('用户数据解析失败:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'sign_in.html';
    }
}

// 退出登录
function logout() {
    // 清除本地存储的登录信息
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // 跳转到登录页面
    window.location.href = 'sign_in.html';
}

// 显示提示信息
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

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    // 检查登录状态
    checkLoginStatus();
    
    // 绑定退出登录按钮
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('确定要退出登录吗？')) {
                logout();
            }
        });
    }
    
    // 显示欢迎信息
    const user = localStorage.getItem('user');
    if (user) {
        try {
            const userData = JSON.parse(user);
            showToast(`欢迎回来，${userData.username}！`, 'success');
        } catch (error) {
            console.error('用户数据解析失败:', error);
        }
    }
});



