import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()


def get_verification_link(email):
    hunter_api_key = os.environ.get('hunter_api_key')
    return f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_key}'


async def check_email(email):
    url = get_verification_link(email)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.json()
            if resp['data']['status'] == 'valid':
                return True
            else:
                return False
