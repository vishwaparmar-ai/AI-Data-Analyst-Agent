# from fastapi import APIRouter,File,UploadFile,Depends
# from backend.utils.validators import validate_file
# from backend.database.dependency import get_current_user
# from backend.models.user import User
# from sqlalchemy.orm import Session
# from backend.database.dependency import get_db
# from backend.models.dataset import Dataset
# from backend.services.data_processing import DatasetAnalyzer
# from backend.agents.data_cleaning_agent import DataCleaningAgent

# import os, shutil

# router = APIRouter(prefix="/upload", tags=["File Upload"])

# UPLOAD_DIR="uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/file_upload")
# async def upload_file(file: UploadFile = File(...), current_user : User = Depends(get_current_user),
#                       db: Session = Depends(get_db) ):

#     await validate_file(file)

#     file_path = os.path.join(UPLOAD_DIR,file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     file_size = os.path.getsize(file_path)

#     processor = DatasetAnalyzer()

#     metadata = processor.process_file(file_path)



#     dataset = Dataset(
#         user_id=current_user.id,
#         file_name=file.filename,
#         file_path=file_path,
#         file_type=file.content_type,
#         file_size=file_size,
#         total_rows=metadata["rows"],
#         total_columns=metadata["columns"],
#         dataset_metadata=metadata
#     )

#     db.add(dataset)
#     db.commit()
#     db.refresh(dataset)

#     agent = DataCleaningAgent()
#     result = agent.run(file_path)

#     # Update cleaned file path
#     dataset.cleaned_filepath = result["cleaned_dataset_path"]

#     # Update cleaned summary
#     dataset.cleaning_summary = result["cleaned_summary"]

#     db.commit()
#     db.refresh(dataset)


#     return {
#         "message": "File uploaded successfully!",
#         "filename": file.filename
#     }


from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from backend.utils.validators import validate_file
from backend.database.dependency import get_current_user, get_db
from backend.models.user import User
from backend.models.dataset import Dataset
from backend.agents.data_cleaning_agent import DataCleaningAgent

import os
import shutil

router = APIRouter(prefix="/upload", tags=["File Upload"])

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/file_upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    await validate_file(file)

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    # Run AI Cleaning Agent
    agent = DataCleaningAgent()

    result = agent.run(file_path)

    # Save dataset information
    dataset = Dataset(
        user_id=current_user.id,
        file_name=file.filename,
        file_path=file_path,
        cleaned_filepath=result["cleaned_dataset_path"],
        file_type=file.content_type,
        file_size=file_size,
        total_rows=result["report"]["rows"],
        total_columns=result["report"]["columns"],
        dataset_metadata=result["report"],
        cleaning_summary=result["cleaned_summary"]
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {
        "message": "Dataset uploaded and cleaned successfully.",
            }

