// Danh sách tài khoản mẫu
const users = [
    { username: "NguyenVanA", email: "nguyenvana@gmail.com" }
];
let generatedOTP = "";

document.getElementById("usernameForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const user = users.find(u => u.username === username);
    const errorDiv = document.getElementById("usernameError");
    if (!user) {
        errorDiv.textContent = "Username does not exist!";
        errorDiv.style.display = "block";
    } else {
        errorDiv.style.display = "none";
        // Giả lập gửi OTP
        generatedOTP = Math.floor(100000 + Math.random() * 900000).toString();
        alert("OTP đã gửi tới email: " + user.email + "\n(OTP demo: " + generatedOTP + ")");
        document.getElementById("section-username").style.display = "none";
        document.getElementById("section-otp").style.display = "block";
    }
});

document.getElementById("otpForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const otp = document.getElementById("otp").value.trim();
    const otpMsg = document.getElementById("otpMessage");
    if (otp === generatedOTP) {
        otpMsg.textContent = "OTP xác thực thành công! Bạn có thể đặt lại mật khẩu.";
        otpMsg.className = "text-success mt-2";
        // Hiện form đổi mật khẩu mới
        setTimeout(() => {
            document.getElementById("section-otp").innerHTML = `
            <form id="resetPasswordForm">
              <div class="mb-3">
                <label for="newPassword" class="form-label">Nhập mật khẩu mới</label>
                <input type="password" class="form-control" id="newPassword" placeholder="Mật khẩu mới" required />
              </div>
              <button type="submit" class="btn btn-success w-100">Đặt lại mật khẩu</button>
              <div id="resetMsg" class="mt-2"></div>
            </form>
          `;
            document.getElementById("resetPasswordForm").addEventListener("submit", function (e) {
                e.preventDefault();
                const newPass = document.getElementById("newPassword").value.trim();
                const resetMsg = document.getElementById("resetMsg");
                if (newPass.length < 8) {
                    resetMsg.textContent = "Mật khẩu phải tối thiểu 8 ký tự.";
                    resetMsg.className = "text-danger mt-2";
                } else {
                    resetMsg.textContent = "Đổi mật khẩu thành công!";
                    resetMsg.className = "text-success mt-2";
                    // Thực tế sẽ gọi API đổi mật khẩu ở đây
                }
            });
        }, 1000);
    } else {
        otpMsg.textContent = "OTP không đúng. Vui lòng thử lại.";
        otpMsg.className = "text-danger mt-2";
    }
});
