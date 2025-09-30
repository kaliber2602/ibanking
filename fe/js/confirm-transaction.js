document.addEventListener('DOMContentLoaded', async function () {
  const username = localStorage.getItem('username');       // ví dụ: "khachhang123"
  const studentId = localStorage.getItem('studentId');     // ví dụ: "SV001"
  alert(studentId);
  alert(username);
  if (!username || !studentId) {
    alert('Thiếu thông tin đăng nhập hoặc sinh viên.');
    return;
  }

  // Gọi FastAPI để lấy thông tin từ PHP
  try {
    const res = await fetch('/get-trans-info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, student_id: studentId })
    });

    const result = await res.json();

    if (!result.success) {
      alert(result.message || 'Không thể lấy thông tin.');
      return;
    }

    const user = result.data.user;
    const student = result.data.student;

    // Lưu vào localStorage nếu cần
    localStorage.setItem('userInfo', JSON.stringify(user));
    localStorage.setItem('studentInfo', JSON.stringify(student));

    // Render thông tin người dùng
    document.getElementById('userFullName').textContent = user.full_name;
    document.getElementById('userEmail').textContent = user.email;
    document.getElementById('userBalance').textContent = user.balance.toLocaleString() + ' VND';

    // Render thông tin sinh viên
    document.getElementById('studentId').textContent = student.student_id;
    document.getElementById('studentFullName').textContent = student.full_name;
    document.getElementById('studentClass').textContent = student.faculty + ' - ' + student.semester;
    document.getElementById('studentTuition').textContent = student.amount.toLocaleString() + ' VND';

    // Render ngày xác nhận
    const now = new Date();
    const dateStr = now.toLocaleDateString('vi-VN') + ' ' + now.toLocaleTimeString('vi-VN');
    document.getElementById('confirmDate').textContent = dateStr;

    // Xử lý nút xác nhận thanh toán
    document.getElementById('confirmBtn').onclick = async function () {
      const confirmRes = await fetch('/confirm-payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          student_id: student.student_id,
          amount: student.amount
        })
      });

      const confirmResult = await confirmRes.json();

      if (confirmRes.ok) {
        alert(confirmResult.message);
        user.balance = confirmResult.newBalance;
        localStorage.setItem('userInfo', JSON.stringify(user));
        window.location.href = '/fe/pages/success.html';
      } else {
        alert(confirmResult.detail || 'Thanh toán thất bại.');
      }
    };
  } catch (error) {
    console.error(error);
    alert('Lỗi kết nối đến máy chủ.');
  }
});
