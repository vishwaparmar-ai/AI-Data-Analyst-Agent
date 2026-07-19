from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.dependency import get_db, get_current_user
from backend.models.user import User
from backend.models.dataset import Dataset
from backend.agents.insights_agent import InsightAgent


router = APIRouter(
    prefix="/insight",
    tags=["Insight Agent"]
)


@router.post("/{dataset_id}")
async def generate_insights(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find dataset
    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id,
            Dataset.user_id == current_user.id
        )
        .first()
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    # Check cleaned dataset
    if not dataset.cleaned_filepath:
        raise HTTPException(
            status_code=400,
            detail="Cleaned dataset not available."
        )

    # Check dataset type
    if not dataset.dataset_type:
        raise HTTPException(
            status_code=400,
            detail="Dataset type not available."
        )

    # Check business summary
    if not dataset.business_summary:
        raise HTTPException(
            status_code=400,
            detail="Business summary not available."
        )

    # Run Insight Agent
    agent = InsightAgent()

    result = agent.run(
        file_path=dataset.cleaned_filepath,
        dataset_type=dataset.dataset_type,
        business_summary=dataset.business_summary
    )

    return {
        "dataset_id": dataset.id,
        "dataset_type": result["dataset_type"],
        "business_summary": result["business_summary"],
        "executive_summary": result["executive_summary"],
        "insights": result["insights"],
        "recommendations": result["recommendations"]
    }