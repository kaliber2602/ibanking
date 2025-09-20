// User mẫu cho phần User Information
const userInfo = {
    fullName: 'Phạm Minh C',
    email: 'phamminhc@kth.edu.vn',
    balance: 12000000
};

// Hàm load dữ liệu user lên các box
function loadUserInfo() {
    const fullNameBox = document.getElementById('fullName');
    const emailBox = document.getElementById('emailAddress');
    const balanceBox = document.getElementById('systemBalance');
    if (fullNameBox) fullNameBox.value = userInfo.fullName;
    if (emailBox) emailBox.value = userInfo.email;
    if (balanceBox) balanceBox.value = userInfo.balance.toLocaleString() + ' VND';
    // Đảm bảo các trường không chỉnh sửa được
    if (fullNameBox) fullNameBox.readOnly = true;
    if (emailBox) emailBox.readOnly = true;
    if (balanceBox) balanceBox.readOnly = true;
}

// Gọi hàm loadUserInfo khi trang đã load xong
window.addEventListener('DOMContentLoaded', loadUserInfo);
// dashboard.js
// Xử lý tìm kiếm và hiển thị popup thông tin sinh viên

// Data mẫu sinh viên
const students = [
    {
        id: '20210001',
        fullName: 'Nguyễn Văn A',
        class: 'K65CNTT',
        email: 'nguyenvana@kth.edu.vn',
        tuition: 5000000
    },
    {
        id: '20210002',
        fullName: 'Trần Thị B',
        class: 'K65QTKD',
        email: 'tranthib@kth.edu.vn',
        tuition: 4500000
    }
];

// Hàm tìm sinh viên theo ID - api
function findStudentById(id) {
    return students.find(sv => sv.id === id);
}

// Hàm render popup thông tin sinh viên
function showStudentPopup(student) {
    // Tạo nội dung popup
    const popupHtml = `
        <div id="studentPopup" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;z-index:9999;">
            <div style="background:#fff;padding:32px 24px;border-radius:8px;min-width:320px;max-width:90vw;box-shadow:0 2px 16px rgba(0,0,0,0.2);position:relative;">
                <button id="closePopupBtn" style="position:absolute;top:8px;right:8px;font-size:20px;background:none;border:none;cursor:pointer;">&times;</button>
                <h4 class="mb-3">Thông tin sinh viên</h4>
                <ul style="list-style:none;padding:0;">
                    <li><b>Mã số sinh viên:</b> ${student.id}</li>
                    <li><b>Họ và tên:</b> ${student.fullName}</li>
                    <li><b>Lớp:</b> ${student.class}</li>
                    <li><b>Email:</b> ${student.email}</li>
                    <li><b>Số tiền cần đóng học phí:</b> ${student.tuition.toLocaleString()} VND</li>
                </ul>
                <div class="d-flex justify-content-end gap-2 mt-4">
                    <button id="cancelPopupBtn" class="btn btn-secondary">Cancel</button>
                    <button id="payPopupBtn" class="btn btn-primary">Thanh toán</button>
                </div>
            </div>
        </div>
    `;
    // Thêm popup vào body
    document.body.insertAdjacentHTML('beforeend', popupHtml);
    // Đóng popup khi bấm nút X hoặc Cancel
    document.getElementById('closePopupBtn').onclick = function () {
        document.getElementById('studentPopup').remove();
    };
    document.getElementById('cancelPopupBtn').onclick = function () {
        document.getElementById('studentPopup').remove();
    };
    // Đóng popup khi click ra ngoài
    document.getElementById('studentPopup').onclick = function (e) {
        if (e.target.id === 'studentPopup') this.remove();
    };
    // Xử lý nút Thanh toán (chưa làm gì, chỉ log ra console)
    document.getElementById('payPopupBtn').onclick = function () {
        // Lưu dữ liệu user và sinh viên vào localStorage
        localStorage.setItem('userInfo', JSON.stringify(userInfo));
        localStorage.setItem('studentInfo', JSON.stringify(student));
        // Chuyển sang trang xác nhận
        window.location.href = '../html/confirm.html';
    };
}

// Xử lý sự kiện form tìm kiếm
const searchForm = document.getElementById('searchForm');
if (searchForm) {
    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        handleStudentSearch();
    });
    // Thêm sự kiện click trực tiếp cho nút Search
    const searchBtn = searchForm.querySelector('button[type="submit"]');
    if (searchBtn) {
        searchBtn.addEventListener('click', function (e) {
            e.preventDefault();
            handleStudentSearch();
        });
    }
}

// Hàm xử lý tìm kiếm sinh viên
function handleStudentSearch() {
    const studentID = document.getElementById('studentID').value.trim();
    const student = findStudentById(studentID);
    if (student) {
        showStudentPopup(student);
        document.getElementById('studentResult').innerHTML = '';
    } else {
        document.getElementById('studentResult').innerHTML = '<div class="alert alert-danger">Không tìm thấy sinh viên!</div>';
    }
}
