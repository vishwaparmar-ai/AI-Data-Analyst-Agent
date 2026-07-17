from fastapi import FastAPI
from backend.api.file_upload import router as file_upload_router
from backend.api.auth import router as auth_router

app = FastAPI()

app.include_router(file_upload_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message":"API is working"}