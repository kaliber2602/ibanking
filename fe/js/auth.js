document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    // Validate không để trống
    if (!username || !password) {
      alert("Vui lòng nhập đầy đủ username và Mật khẩu.");
      return;
    }

    // Validate password tối thiểu 8 ký tự
    if (password.length < 8) {
      alert("Mật khẩu phải có ít nhất 8 ký tự.");
      return;
    }

    // Kiểm tra tài khoản mẫu
    if (username === "NguyenVanA" && password === "12345678") {
      alert("Đăng nhập thành công!");
      // Thực hiện chuyển trang hoặc các thao tác tiếp theo ở đây
    } else {
      alert("Sai tài khoản hoặc mật khẩu.");
    }
  });
});