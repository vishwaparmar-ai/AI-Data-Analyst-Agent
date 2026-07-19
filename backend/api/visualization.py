from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependency import get_current_user
from backend.database.dependency import get_db

from backend.models.user import User
from backend.models.dataset import Dataset

from backend.schemas.user import QueryRequest

from backend.agents.sql_agent import SQLAgent
from backend.agents.visualization_agent import VisualizationAgent


router = APIRouter(
    prefix="/visualization",
    tags=["Visualization Agent"]
)


@router.post("/")
async def generate_visualization(
    req: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

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

    if not dataset.cleaned_filepath:
        raise HTTPException(
            status_code=400,
            detail="Cleaned dataset not found."
        )

    sql_agent = SQLAgent()

    sql_result = sql_agent.run(
        file_path=dataset.cleaned_filepath,
        question=req.question
    )

    dataframe = sql_result["dataframe"]

    visualization_agent = VisualizationAgent()

    visualization_result = visualization_agent.run(
        question=req.question,
        dataframe=dataframe
    )

    return {
        "dataset_id": dataset.id,
        "question": req.question,
        "chart_plan": visualization_result["chart_plan"],
        "chart_path": visualization_result["chart_path"]
    }