import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_visualization(token, dataset_id, question):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "dataset_id": dataset_id,
        "question": question
    }

    response = requests.post(
        f"{BASE_URL}/visualization",
        json=payload,
        headers=headers
    )

    return response