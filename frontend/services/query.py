import requests

BASE_URL = "http://127.0.0.1:8000"


def query_dataset(token, dataset_id, question):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "dataset_id": dataset_id,
        "question": question
    }

    response = requests.post(
        f"{BASE_URL}/query",
        json=payload,
        headers=headers
    )

    return response