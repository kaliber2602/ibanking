from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
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
SEND_OTP_URL = "http://localhost/ibanking-app/be/php-backend/send-otp.php"
VERIFY_OTP_URL = "http://localhost/ibanking-app/be/php-backend/verify-otp.php"
RESET_PASSWORD_URL = "http://localhost/ibanking-app/be/php-backend/reset-password.php"
GET_TRANS_INFO_URL = "http://localhost/ibanking-app/be/php-backend/get-trans-infor.php"
CONFIRM_PAYMENT_URL = "http://localhost/ibanking-app/be/php-backend/gateway.php"

# Static files
app.mount("/fe/css", StaticFiles(directory="fe/css"), name="css")
app.mount("/fe/js", StaticFiles(directory="fe/js"), name="js")
app.mount("/fe/imgs", StaticFiles(directory="fe/imgs"), name="imgs")

# Pages
@app.get("/", response_class=HTMLResponse)
def home():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return templates.TemplateResponse("dashboard.html", {"request": {}})

@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password():
    return templates.TemplateResponse("forgot-password.html", {"request": {}})

@app.get("/confirm-transaction", response_class=HTMLResponse)
def confirm_transaction():
    return templates.TemplateResponse("confirm-transaction.html", {"request": {}})

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class UsernameRequest(BaseModel):
    username: str

class OTPRequest(BaseModel):
    username: str
    otp: str

class EmailRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str

class TransInfoRequest(BaseModel):
    username: str
    student_id: str
# demo
class ConfirmPaymentRequest(BaseModel):
    username: str
    student_id: str
    amount: float
# Auth
@app.post("/login")
async def login(payload: LoginRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(AUTH_SERVICE_URL, json=payload.dict(), timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Auth Service: {str(e)}"}, status_code=500)

    if result.get("success"):
        return JSONResponse(content={"success": True, "redirect": "/dashboard", "username": payload.username})
    return JSONResponse(content={"success": False, "message": result.get("message", "Đăng nhập thất bại.")}, status_code=401)

# User Info
@app.get("/user-info")
async def get_user_info(username: str = Query(..., description="Tên đăng nhập cần lấy thông tin")):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(CUSTOMER_INFO_URL, json={"username": username}, timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Customer Service: {str(e)}"}, status_code=500)

    if result.get("success"):
        return JSONResponse(content={"success": True, "data": result.get("data")})
    return JSONResponse(content={"success": False, "message": result.get("message", "Không thể lấy thông tin người dùng.")}, status_code=404)

# Transaction History
@app.post("/transactions")
async def get_transactions(payload: UsernameRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(TRANSACTION_SERVICE_URL, json=payload.dict(), timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Transaction Service: {str(e)}"}, status_code=500)
    return JSONResponse(content=result)

# Find Student Info
@app.get("/gateway/find-student.php")
async def find_student(id: str = Query(..., description="Mã số sinh viên")):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{FIND_STUDENT_URL}?id={id}", timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Find Student Service: {str(e)}"}, status_code=500)

    if result.get("success"):
        return JSONResponse(content={"success": True, "data": result.get("data")})
    return JSONResponse(content={"success": False, "message": result.get("message", "Không tìm thấy sinh viên.")}, status_code=404)

# Check Username
@app.post("/check-username")
async def check_username(payload: UsernameRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(CHECK_USERNAME_URL, json=payload.dict(), timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối: {str(e)}"}, status_code=500)
    return JSONResponse(content=result)

# Get Email
@app.post("/get-email")
async def get_email(payload: UsernameRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(GET_EMAIL_URL, json=payload.dict(), timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối: {str(e)}"}, status_code=500)
    return JSONResponse(content=result)

# Send OTP
@app.post("/send-otp")
async def send_otp(payload: EmailRequest):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                SEND_OTP_URL,
                json=payload.dict()
            )
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception:
        return JSONResponse(
            content={"success": False, "message": "Phản hồi từ PHP không hợp lệ"},
            status_code=500
        )

# Verify OTP
@app.post("/verify-otp")
async def verify_otp(payload: OTPRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(VERIFY_OTP_URL, json=payload.dict())
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception:
        return JSONResponse(content={"success": False, "message": "Phản hồi không hợp lệ"}, status_code=500)

# Reset Password
@app.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(RESET_PASSWORD_URL, json=payload.dict())
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception:
        return JSONResponse(content={"success": False, "message": "Phản hồi không hợp lệ từ PHP"}, status_code=500)

@app.post("/get-trans-info")
async def get_trans_info(payload: TransInfoRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(GET_TRANS_INFO_URL, json=payload.dict(), timeout=5.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối GetTransInfo Service: {str(e)}"}, status_code=500)

    if result.get("success"):
        return JSONResponse(content=result)
    return JSONResponse(content={"success": False, "message": result.get("message", "Không thể lấy thông tin.")}, status_code=404)

@app.post("/confirm-payment")
async def confirm_payment(payload: ConfirmPaymentRequest):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(CONFIRM_PAYMENT_URL, json=payload.dict(), timeout=3.0)
            result = resp.json()
    except httpx.RequestError as e:
        return JSONResponse(content={"success": False, "message": f"Lỗi kết nối Gateway Service: {str(e)}"}, status_code=500)

    if result.get("success"):
        return JSONResponse(content=result)
    return JSONResponse(content={"success": False, "message": result.get("message", "Thanh toán thất bại.")}, status_code=400)