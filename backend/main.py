from fastapi import FastAPI
from backend.api.file_upload import router as file_upload_router
from backend.api.auth import router as auth_router
from backend.api.user_query import router as sql_router
from backend.api.visualization import router as visualization_router
from backend.api.insight import router as insight_router
from backend.api.report import router as report_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Data Analyst")


app.mount("/generated_charts", StaticFiles(directory="generated_charts"), name="generated_charts")
app.include_router(file_upload_router)
app.include_router(auth_router)
app.include_router(sql_router)
app.include_router(visualization_router)
app.include_router(insight_router)
app.include_router(report_router)




@app.get("/")
def home():
    return {"message":"API is working"}