pip install fastapi
pip install "uvicorn[standard]"  #bắt buộc để chạy ứng dụng FastAPI
pip install pydantic
pip install httpx
pip install fastapi[all]


python -m uvicorn frontend_service.main:app --port 8000 --reload
python -m uvicorn auth_service.main:app --port 8001 --reload
python -m uvicorn user_service.main:app --port 8002 --reload
python -m uvicorn otp_service.main:app --port 8003 --reload
python -m uvicorn transaction_service.main:app --port 8004 --reload
python -m uvicorn student_service.main:app --port 8005 --reload
