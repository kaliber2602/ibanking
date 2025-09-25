document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const forgotPasswordLink = document.getElementById("forgotPasswordLink");

  // Xử lý đăng nhập
  loginForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
      alert("Vui lòng nhập đầy đủ username và mật khẩu.");
      return;
    }

    if (password.length < 8) {
      alert("Mật khẩu phải có ít nhất 8 ký tự.");
      return;
    }

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
      });

      const result = await response.json();

      if (result.success && result.redirect) {
        localStorage.setItem("username", username);
        window.location.href = result.redirect;
      } else {
        alert(result.message || "Đăng nhập thất bại.");
      }
    } catch (error) {
      alert("Lỗi kết nối tới máy chủ. Vui lòng thử lại sau.");
    }
  });

  if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = "/forgot-password";
    });
  }
});
