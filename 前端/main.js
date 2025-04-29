const API_BASE_URL = 'http://localhost:5000';
// 退出登录功能
function logout() {
    fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'logout' })
    })
    .then(response => {
        if (response.ok) {
            alert('退出登录成功！');
            window.location.href = '/sign_in.html'; // 跳转到登录页面
        } else {
            alert('退出登录失败，请重试！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('网络错误，请稍后重试！');
    });
}