const API_BASE_URL = 'http://localhost:5000'; // 确保在生产环境中替换为正确的地址
const jwtToken = localStorage.getItem('jwt_token'); // 从本地存储获取 JWT Token

// 退出登录功能
function logout() {
    fetch(`${API_BASE_URL}/api/user/logout`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${jwtToken}` // 使用 jwtToken 变量
        },
        body: JSON.stringify({ action: 'logout' }) // 确认后端是否需要 body
    })
    .then(response => {
        if (response.ok) {
            alert('退出登录成功！');
            window.location.href = '/sign_in.html'; // 跳转到登录页面
        } else {
            // 根据状态码提供更具体的错误提示
            if (response.status === 401) {
                alert('未授权，请重新登录！');
            } else {
                alert('退出登录失败，请重试！');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('网络错误，请稍后重试！');
    });
}