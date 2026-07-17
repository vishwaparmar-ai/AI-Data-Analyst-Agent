from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def validate_file(file: UploadFile):
    # Check if file is provided
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    # Validate extension
    extension = "." + file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are allowed."
        )

    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type."
        )

    # Validate file size
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )

    # Reset file pointer
    file.file.seek(0)

    return True