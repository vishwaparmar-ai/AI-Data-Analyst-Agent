from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from backend.database.dependency import get_db, get_current_user
from backend.models.user import User
from backend.models.dataset import Dataset
from backend.agents.report_agent import ReportAgent


router = APIRouter(
    prefix="/report",
    tags=["Report Agent"]
)


@router.post("/{dataset_id}")
async def generate_report(
    dataset_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

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

    if not dataset.cleaned_filepath:
        raise HTTPException(
            status_code=400,
            detail="Cleaned dataset not available."
        )

    if not dataset.business_summary:
        raise HTTPException(
            status_code=400,
            detail="Business summary not available."
        )

    agent = ReportAgent()

    result = agent.run(dataset)

    return FileResponse(
        path=result["report_path"],
        filename=os.path.basename(result["report_path"]),
        media_type="application/pdf"
    )