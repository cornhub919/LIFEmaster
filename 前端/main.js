// 检查登录状态和初始化
document.addEventListener('DOMContentLoaded', function(){
    // 检查用户是否已登录
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    if (!token || !user) {
        window.location.href = 'sign_in.html';
        return;
    }
    try {
        // 显示用户名
        const userData = JSON.parse(user);
        const welcomeElement = document.getElementById('user-welcome');
        if (welcomeElement) {
            welcomeElement.textContent = `欢迎，${userData.username}！`;
        }
    } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'sign_in.html';
    }
});

// 退出登录
function logout() {
    if (confirm('确定要退出登录吗？')) {
        const token = localStorage.getItem('token');
        fetch('http://localhost:5000/api/auth/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }).finally(() => {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            showToast('已成功退出登录', 'success');
            setTimeout(() => {
                window.location.href = 'sign_in.html';
            }, 1500);
        });
    }
}

// 显示模块
function showModule(moduleId, event) {
    // 隐藏所有模块
    const modules = document.querySelectorAll('.module');
    modules.forEach(module => module.classList.remove('active'));

    // 移除所有菜单项的active类
    const menuItems = document.querySelectorAll('.menu a');
    menuItems.forEach(item => item.classList.remove('active'));

    // 显示指定模块
    document.getElementById(moduleId + '-module').classList.add('active');

    // 添加对应菜单项的active类
    if (event && event.target) {
        event.target.classList.add('active');
    }

    // 根据模块加载相应数据
    switch(moduleId) {
        case 'tasks':
            loadTasks();
            break;
        case 'accounting':
            loadAccountingData();
            break;
        case 'handbook':
            loadHandbooks();
            break;
    }
}

// 应用初始化
function initializeApp() {
    // 设置今天的日期为默认值
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('record-date');
    if (dateInput) {
        dateInput.value = today;
    }

    // 默认加载待办事项
    loadTasks();
}

// 待办事项相关函数
async function addNewTask() {
    const taskText = document.getElementById('new-task').value.trim();
    const deadline = document.getElementById('task-deadline').value;

    if (!taskText) {
        showToast('请输入任务内容', 'error');
        return;
    }

    await addTask(taskText, deadline || null);

    // 清空输入框
    document.getElementById('new-task').value = '';
    document.getElementById('task-deadline').value = '';
}

function displayTasks(data) {
    const tasksList = document.getElementById('tasks-list');
    const tasks = data.tasks || [];

    if (tasks.length === 0) {
        tasksList.innerHTML = '<div class="empty-message">暂无待办事项</div>';
        return;
    }

    tasksList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <input type="checkbox" ${task.completed ? 'checked' : ''} 
                   onchange="toggleTask(${task.id}, this.checked)">
            <span class="task-text">${task.text}</span>
            ${task.deadline ? `<span class="task-deadline">${new Date(task.deadline).toLocaleString()}</span>` : ''}
            <button class="delete-btn" onclick="deleteTask(${task.id})">删除</button>
        </div>
    `).join('');
}

// 记账相关函数
async function addNewRecord() {
    const type = document.getElementById('record-type').value;
    const categoryId = document.getElementById('record-category').value;
    const amount = document.getElementById('record-amount').value;
    const date = document.getElementById('record-date').value;
    const note = document.getElementById('record-note').value;

    if (!categoryId || !amount || !date) {
        showToast('请填写完整信息', 'error');
        return;
    }

    if (parseFloat(amount) <= 0) {
        showToast('金额必须大于0', 'error');
        return;
    }

    const recordData = {
        type: type,
        category_id: categoryId,
        amount: parseFloat(amount),
        date: date,
        note: note
    };

    await addAccountingRecord(recordData);

    // 清空输入框
    document.getElementById('record-amount').value = '';
    document.getElementById('record-note').value = '';
}

function displayCategories(data) {
    const categorySelect = document.getElementById('record-category');
    const typeSelect = document.getElementById('record-type');

    function updateCategories() {
        const selectedType = typeSelect.value;
        const categories = data[selectedType] || [];

        categorySelect.innerHTML = categories.map(cat =>
            `<option value="${cat.id}">${cat.name}</option>`
        ).join('');

        if (categories.length === 0) {
            categorySelect.innerHTML = '<option value="">暂无分类</option>';
        }
    }

    // 初始化分类选项
    updateCategories();

    // 监听类型变化
    typeSelect.addEventListener('change', updateCategories);
}

function displayRecords(records, categories) {
    const recordsList = document.getElementById('records-list');
    if (!Array.isArray(records)) records = [];
    if (records.length === 0) {
        recordsList.innerHTML = '<div class="empty-message">暂无记账记录</div>';
        return;
    }
    recordsList.innerHTML = records.map(record => {
        let cat = null;
        if (categories && categories[record.type]) {
            cat = categories[record.type].find(c => String(c.id) === String(record.category_id));
        }
        return `
        <div class="record-item ${record.type}">
            <div class="record-info">
                <span class="record-type">${record.type === 'income' ? '收入' : '支出'}</span>
                <span class="record-category">${cat ? cat.name : '未知分类'}</span>
                <span class="record-amount ${record.type}">${record.type === 'income' ? '+' : '-'}¥${record.amount}</span>
            </div>
            <div class="record-details">
                <span class="record-date">${record.date}</span>
                ${record.note ? `<span class="record-note">${record.note}</span>` : ''}
            </div>
        </div>
        `;
    }).join('');
}

// 手账相关函数
async function addNewHandbook() {
    const title = document.getElementById('handbook-title').value.trim();
    const content = document.getElementById('handbook-content').value.trim();

    if (!title) {
        showToast('请输入手账标题', 'error');
        return;
    }

    await addHandbook(title, content);

    // 清空输入框
    document.getElementById('handbook-title').value = '';
    document.getElementById('handbook-content').value = '';
}

function displayHandbooks(data) {
    const handbooksList = document.getElementById('handbooks-list');
    const handbooks = data.handbooks || [];

    if (handbooks.length === 0) {
        handbooksList.innerHTML = '<div class="empty-message">暂无手账记录</div>';
        return;
    }

    handbooksList.innerHTML = handbooks.map(handbook => `
        <div class="handbook-item">
            <div class="handbook-header">
                <h3>${handbook.title}</h3>
                <span class="handbook-date">${new Date(handbook.created_at).toLocaleDateString()}</span>
                <button class="delete-btn" onclick="deleteHandbook(${handbook.id})">删除</button>
            </div>
            <div class="handbook-content">${handbook.content.replace(/\n/g, '<br>')}</div>
        </div>
    `).join('');
}



