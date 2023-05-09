import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_verification_link(email):
    hunter_api_key = os.environ.get("hunter_api_key")
    return f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_key}"


def check_email(email):
    url = get_verification_link(email)
    response = requests.get(url)
    resp = response.json()
    if resp["data"]["status"] != "valid":
        return False
    return True
