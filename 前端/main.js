const API_BASE_URL = 'http://localhost:5000'; // 确保在生产环境中替换为正确的地址
const jwtToken = localStorage.getItem('jwt_token'); // 从本地存储获取 JWT Token
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

// 获取退出登录按钮
const logoutButton = document.querySelector('.logout-btn');

// 为按钮添加点击事件
logoutButton.addEventListener('click', () => {
    logout(); // 调用退出登录函数
});


// 退出登录功能
async function logout() {
    showToast('正在退出登录...'); // 显示提示框
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${jwtToken}` // 使用 jwtToken 变量
            },
            body: JSON.stringify({ action: 'logout' }) // 确认后端是否需要 body
        });

        if (response.ok) {
            showToast('退出登录成功！');
            localStorage.removeItem('jwt_token'); // 清除本地存储中的 JWT Token
            window.location.href = 'sign_in.html'; // 跳转到登录页面
        } else {
            // 根据状态码提供更具体的错误提示
            if (response.status === 401) {
                showToast('未授权，请重新登录！');
            } else {
                showToast('退出登录失败，请重试！');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('网络错误，请稍后重试！');
    }
}

function checkLoginStatus() {
    if (jwtToken) {
        // 如果已登录，直接跳转到主页面
        window.location.href = 'main2.html'; // 替换为 main2.html
    }
}



