import requests

from services.api import BASE_URL


def login(email, password):

    response = requests.post(

        f"{BASE_URL}/auth/login",

        json={
            "email": email,
            "password": password
        }

    )

    return response


def register(username, email, password):

    response = requests.post(

        f"{BASE_URL}/auth/register",

        json={
            "username": username,
            "email": email,
            "password": password
        }

    )

    return response