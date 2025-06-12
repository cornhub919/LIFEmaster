// API工具函数
// API基础URL
const API_BASE_URL = 'https://lifemaster-xxxx.onrender.com';

// 提示函数
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    } else {
        console.log(`提示: ${message} (${type})`);
    }
}

function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// 通用API请求函数
async function apiRequest(url, options = {}) {
    try {
        // 确保url有正确的前缀
        const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`;

        // 默认headers包含认证信息
        const headers = options.headers || getAuthHeaders();
        
        const response = await fetch(fullUrl, {
            ...options,
            headers
        });

        // 若收到 401，跳转到登录
        if (response.status === 401) {
            window.location.href = 'sign_in.html';
            return response;
        }

        return response;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// 待办事项相关函数
async function loadTasks() {
    const response = await apiRequest('/api/tasks');
    if (response && response.ok) {
        const data = await response.json();
        if (typeof displayTasks === 'function') {
            displayTasks(data.data); // 保证 displayTasks(data) 兼容
        }
        return data;
    }
    return null;
}

async function addTask(taskText, deadline = null) {
    // 修复：保持完整的日期时间处理，不要只取日期部分
    let formattedDeadline = null;
    if (deadline && deadline.trim() !== "") {
        try {
            console.log("原始日期:", deadline);
            // 保持完整的datetime-local格式：YYYY-MM-DDTHH:MM
            formattedDeadline = deadline;
            console.log("格式化后的日期:", formattedDeadline);
        } catch (e) {
            console.error('处理日期失败:', e);
            formattedDeadline = null;
        }
    } else {
        console.log("没有提供日期或日期为空");
    }
    
    const taskData = {
        text: taskText,
        deadline: formattedDeadline,
        completed: false
    };
    
    try {
        console.log('API请求添加任务:', taskData);
        // 保证返回 fetch Response 对象
        return await apiRequest('/api/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData)
        });
    } catch (error) {
        console.error('添加任务异常:', error);
        showToast('添加任务异常', 'error');
        throw error;
    }
}

async function toggleTask(taskId, completed) {
    return await apiRequest(`/api/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify({ completed })
    });
}

async function deleteTask(taskId) {
    return await apiRequest(`/api/tasks/${taskId}`, {
        method: 'DELETE'
    });
}

// 记账相关函数（仿照todolist风格，简单明了，便于调试）

// 获取分类
async function loadCategories() {
    const response = await apiRequest('/api/accounting/categories');
    if (response && response.ok) {
        const data = await response.json();
        if (typeof displayCategories === 'function') {
            displayCategories(data.data); // {income:[], expense:[]}
        }
        return data.data;
    }
    showToast('加载分类失败', 'error');
    return null;
}

// 获取记账记录
async function loadRecords() {
    const response = await apiRequest('/api/accounting/records');
    if (response && response.ok) {
        const data = await response.json();
        if (typeof displayRecords === 'function') {
            // 兼容 displayRecords(records, categories)
            displayRecords(data.data.records, window.categories || {});
        }
        return data.data.records;
    }
    showToast('加载记账记录失败', 'error');
    return [];
}

// 统一加载记账数据（分类和记录）
async function loadAccountingData() {
    // 先加载分类
    const categories = await loadCategories();
    window.categories = categories || { income: [], expense: [] };
    // 再加载记录
    await loadRecords();
}

// 添加记账记录
async function addAccountingRecord(recordData) {
    const response = await apiRequest('/api/accounting/records', {
        method: 'POST',
        body: JSON.stringify(recordData)
    });
    if (response && response.ok) {
        const res = await response.json();
        if (res.code === 0) {
            showToast('记账记录添加成功', 'success');
            await loadAccountingData();
        } else {
            showToast(res.msg || '添加失败', 'error');
        }
    } else {
        showToast('添加失败', 'error');
    }
}

// 添加记账分类
async function addAccountingCategory(categoryData) {
    const response = await apiRequest('/api/accounting/categories', {
        method: 'POST',
        body: JSON.stringify(categoryData)
    });
    if (response && response.ok) {
        const res = await response.json();
        if (res.code === 0) {
            showToast('分类添加成功', 'success');
            await loadAccountingData();
        } else {
            showToast(res.msg || '添加失败', 'error');
        }
    } else {
        showToast('添加失败', 'error');
    }
}

// 更新记账记录
async function updateAccountingRecord(recordId, updateData) {
    const response = await apiRequest(`/api/accounting/records/${recordId}`, {
        method: 'PUT',
        body: JSON.stringify(updateData)
    });
    if (response && response.ok) {
        showToast('修改成功', 'success');
        await loadAccountingData();
    } else {
        showToast('修改失败', 'error');
    }
}

// 删除记账记录
async function deleteAccountingRecord(recordId) {
    const response = await apiRequest(`/api/accounting/records/${recordId}`, {
        method: 'DELETE'
    });
    if (response && response.ok) {
        showToast('删除成功', 'success');
        await loadAccountingData();
    } else {
        showToast('删除失败', 'error');
    }
}

// 手账相关函数
async function loadHandbooks() {
    const response = await apiRequest('/api/handbooks');
    if (response && response.ok) {
        const data = await response.json();
        if (typeof displayHandbooks === 'function') {
            displayHandbooks(data);
        }
        return data;
    }
    return null;
}

async function addHandbook(title, content) {
    const handbookData = {
        title: title,
        content: content
    };
    
    const response = await apiRequest('/api/handbooks', {
        method: 'POST',
        body: JSON.stringify(handbookData)
    });
    
    if (response && response.ok) {
        const result = await response.json();
        if (result.code === 0) {
            showToast('手账保存成功', 'success');
            if (typeof loadHandbooks === 'function') {
                loadHandbooks();
            }
            return result;
        } else {
            showToast('保存失败: ' + result.msg, 'error');
            return null;
        }
    } else {
        showToast('保存手账失败', 'error');
        return null;
    }
}

async function updateHandbook(handbookId, title, content) {
    const handbookData = {
        title: title,
        content: content
    };
    
    const response = await apiRequest(`/api/handbooks/${handbookId}`, {
        method: 'PUT',
        body: JSON.stringify(handbookData)
    });
    
    if (response && response.ok) {
        const result = await response.json();
        if (result.code === 0) {
            showToast('手账更新成功', 'success');
            if (typeof loadHandbooks === 'function') {
                loadHandbooks();
            }
            return result;
        } else {
            showToast('更新失败: ' + result.msg, 'error');
            return null;
        }
    } else {
        showToast('更新手账失败', 'error');
        return null;
    }
}

async function deleteHandbook(handbookId) {
    const response = await apiRequest(`/api/handbooks/${handbookId}`, {
        method: 'DELETE'
    });
    
    if (response && response.ok) {
        const result = await response.json();
        if (result.code === 0) {
            showToast('手账删除成功', 'success');
            if (typeof loadHandbooks === 'function') {
                loadHandbooks();
            }
            return result;
        } else {
            showToast('删除失败: ' + result.msg, 'error');
            return null;
        }
    } else {
        showToast('删除手账失败', 'error');
        return null;
    }
}

// 保持main.js和todolist.html等模块的接口兼容性：
// 1. addTask、toggleTask、deleteTask、loadTasks 这些函数名称和参数保持不变
// 2. loadTasks 返回的数据结构为 { data: { tasks: [...] } }，displayTasks(data) 兼容
// 3. addTask 返回 fetch Response，addNewTask/addTaskToAPI 可直接判断 response.ok
// 4. 记账、手账等接口同理，参数和返回结构不变

// 例如：addTask
async function addTask(taskText, deadline = null) {
    // 修复：保持完整的日期时间处理，不要只取日期部分
    let formattedDeadline = null;
    if (deadline && deadline.trim() !== "") {
        try {
            console.log("原始日期:", deadline);
            // 保持完整的datetime-local格式：YYYY-MM-DDTHH:MM
            formattedDeadline = deadline;
            console.log("格式化后的日期:", formattedDeadline);
        } catch (e) {
            console.error('处理日期失败:', e);
            formattedDeadline = null;
        }
    } else {
        console.log("没有提供日期或日期为空");
    }
    
    const taskData = {
        text: taskText,
        deadline: formattedDeadline,
        completed: false
    };
    
    // 保证返回 fetch Response 对象
    return await apiRequest('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(taskData)
    });
}

// 例如：toggleTask
async function toggleTask(taskId, completed) {
    return await apiRequest(`/api/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify({ completed })
    });
}

// 例如：deleteTask
async function deleteTask(taskId) {
    return await apiRequest(`/api/tasks/${taskId}`, {
        method: 'DELETE'
    });
}

// 例如：loadTasks
async function loadTasks() {
    const response = await apiRequest('/api/tasks');
    if (response && response.ok) {
        const data = await response.json();
        if (typeof displayTasks === 'function') {
            displayTasks(data.data); // 保证 displayTasks(data) 兼容
        }
        return data;
    }
    return null;
}