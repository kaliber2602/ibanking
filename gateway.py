from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="fe/html")

# Service URLs
AUTH_SERVICE_URL = "http://localhost/ibanking-app/be/php-backend/auth.php"
CUSTOMER_INFO_URL = "http://localhost/ibanking-app/be/php-backend/customer-infor.php"
TRANSACTION_SERVICE_URL = "http://localhost/ibanking-app/be/php-backend/transaction.php"
FIND_STUDENT_URL = "http://localhost/ibanking-app/be/php-backend/find-student.php"
CHECK_USERNAME_URL = "http://localhost/ibanking-app/be/php-backend/check-username.php"
GET_EMAIL_URL = "http://localhost/ibanking-app/be/php-backend/get-email.php"
# Static files
app.mount("/fe/css", StaticFiles(directory="fe/css"), name="css")
app.mount("/fe/js", StaticFiles(directory="fe/js"), name="js")
app.mount("/fe/imgs", StaticFiles(directory="fe/imgs"), name="imgs")

# Pages
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password(request: Request):
    return templates.TemplateResponse("forgot-password.html", {"request": request})

@app.get("/confirm-transaction", response_class=HTMLResponse)
def confirm_transaction(request: Request):
    return templates.TemplateResponse("confirm-transaction.html", {"request": request})
# Auth
@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                AUTH_SERVICE_URL,
                json={"username": username, "password": password},
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Auth Service: {str(e)}"})

    if result.get("success"):
        return JSONResponse(content={"success": True, "redirect": "/dashboard", "username": username})
    else:
        return JSONResponse(content={"success": False, "message": result.get("message", "Đăng nhập thất bại.")})

# User Info
@app.get("/user-info")
async def get_user_info(request: Request):
    username = request.query_params.get("username")
    if not username:
        return RedirectResponse(url="/", status_code=303)

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                CUSTOMER_INFO_URL,
                json={"username": username},
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Customer Service: {str(e)}"})

    if result.get("success"):
        return JSONResponse(content={"success": True, "data": result.get("data")})
    else:
        return JSONResponse(content={"success": False, "message": result.get("message", "Không thể lấy thông tin người dùng.")})

# Transaction History
@app.post("/transactions")
async def get_transactions(request: Request):
    body = await request.json()
    username = body.get("username")
    if not username:
        return JSONResponse(content={"success": False, "message": "Thiếu username."})

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                TRANSACTION_SERVICE_URL,
                json={"username": username},
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Transaction Service: {str(e)}"})

    return JSONResponse(content=result)

# Find Student Info
@app.get("/gateway/find-student.php")
async def find_student(request: Request):
    student_id = request.query_params.get("id")
    if not student_id:
        return JSONResponse(content={"success": False, "message": "Thiếu mã số sinh viên."})

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{FIND_STUDENT_URL}?id={student_id}",
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Find Student Service: {str(e)}"})

    if result.get("success"):
        return JSONResponse(content={"success": True, "data": result.get("data")})
    else:
        return JSONResponse(content={"success": False, "message": result.get("message", "Không tìm thấy sinh viên.")})

@app.post("/check-username")
async def check_username(request: Request):
    data = await request.json()
    username = data.get("username")

    if not username:
        return JSONResponse(content={"success": False, "message": "Thiếu username"})

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                CHECK_USERNAME_URL,
                json={"username": username},
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối: {str(e)}"})

    return JSONResponse(content=result)

@app.post("/get-email")
async def get_email(request: Request):
    data = await request.json()
    username = data.get("username")

    if not username:
        return JSONResponse(content={"success": False, "message": "Thiếu username"})

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                GET_EMAIL_URL,
                json={"username": username},
                timeout=3.0
            )
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối: {str(e)}"})

    return JSONResponse(content=result)

@app.post("/send-otp")
async def gateway_send_otp(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost/ibanking-app/be/php-backend/send-otp.php",
            json=body,
            headers={"Content-Type": "application/json"}
        )

    try:
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception:
        print("PHP response:", response.text)  # In ra để kiểm tra
        return JSONResponse(
            content={"success": False, "message": "Phản hồi từ PHP không hợp lệ"},
            status_code=500
        )

@app.post("/verify-otp")
async def gateway_verify_otp(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost/ibanking-app/be/php-backend/verify-otp.php",
            json=body,
            headers={"Content-Type": "application/json"}
        )
    try:
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception:
        print("PHP response:", response.text)
        return JSONResponse(content={"success": False, "message": "Phản hồi không hợp lệ"}, status_code=500)

@app.post("/reset-password")
async def gateway_reset_password(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost/ibanking-app/be/php-backend/reset-password.php",
            json=body,
            headers={"Content-Type": "application/json"}
        )
    try:
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception:
        print("PHP response:", response.text)
        return JSONResponse(
            content={"success": False, "message": "Phản hồi không hợp lệ từ PHP"},
            status_code=500
        )