import requests


BASE_URL = "http://127.0.0.1:8000"


def upload_dataset(file, token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (
            file.name,
            file.getvalue(),
            file.type
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload/file_upload",
        headers=headers,
        files=files
    )

    return response