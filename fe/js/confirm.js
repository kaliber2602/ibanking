// confirm.js
// Lấy dữ liệu user và sinh viên từ localStorage và render ra các trường

document.addEventListener('DOMContentLoaded', function () {
    // Lấy dữ liệu từ localStorage
    const user = JSON.parse(localStorage.getItem('userInfo'));
    const student = JSON.parse(localStorage.getItem('studentInfo'));

    // Render thông tin user
    if (user) {
        document.getElementById('userFullName').textContent = user.fullName;
        document.getElementById('userEmail').textContent = user.email;
        document.getElementById('userBalance').textContent = user.balance.toLocaleString() + ' VND';
    }
    // Render thông tin sinh viên
    if (student) {
        document.getElementById('studentId').textContent = student.id;
        document.getElementById('studentFullName').textContent = student.fullName;
        document.getElementById('studentClass').textContent = student.class;
        document.getElementById('studentEmail').textContent = student.email;
        document.getElementById('studentTuition').textContent = student.tuition.toLocaleString() + ' VND';
    }
    // Render ngày xác nhận
    const now = new Date();
    const dateStr = now.toLocaleDateString('vi-VN') + ' ' + now.toLocaleTimeString('vi-VN');
    document.getElementById('confirmDate').textContent = dateStr;

    // Xử lý nút xác nhận thanh toán
    document.getElementById('confirmBtn').onclick = function () {
        alert('Thanh toán thành công!');
        // Có thể chuyển hướng hoặc xử lý tiếp tại đây
    };
});
