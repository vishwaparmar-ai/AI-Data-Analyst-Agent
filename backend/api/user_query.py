from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.dependency import get_db
from backend.database.dependency import get_current_user
from backend.models.user import User
from backend.models.dataset import Dataset
from backend.agents.sql_agent import SQLAgent
from backend.schemas.user import QueryRequest


router = APIRouter(
    prefix="/query",
    tags=["SQL Agent"]
)

@router.post("/")
async def query_dataset(req:QueryRequest, current_user: User = Depends(get_current_user), 
                        db:Session = Depends(get_db)):
    # Find dataset
    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == req.dataset_id,
            Dataset.user_id == current_user.id
        )
        .first()
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    # Ensure cleaned dataset exists
    if not dataset.cleaned_filepath:
        raise HTTPException(
            status_code=400,
            detail="Cleaned dataset not available."
        )

    # Run SQL Agent
    agent = SQLAgent()

    result = agent.run(
        file_path=dataset.cleaned_filepath,
        question=req.question
    )

    return {
        "dataset_id": dataset.id,
        "question": result["question"],
        "generated_sql": result["sql_query"],
        "results": result["result"]
    }
