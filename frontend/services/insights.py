import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_insights(
    token: str,
    dataset_id: int
):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        f"{BASE_URL}/insight/{dataset_id}",
        headers=headers
    )

    return response