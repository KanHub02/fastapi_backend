import requests
import aiohttp
from decouple import config as env


API_KEY = env("API_KEY")


class RequestService:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    data = {"model": "gpt-3.5-turbo"}

    @classmethod
    async def send_async_request(cls, question: str) -> requests:
        async with aiohttp.ClientSession() as session:
            cls.data.update({"messages": [{"role": "user", "content": question}]})
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=cls.headers,
                json=cls.data,
            ) as response:
                answer = (
                    await response.json().get("choices")[0]["message"].get("content")
                )
                return answer

    @classmethod
    def send_request(cls, question: str) -> requests:
        cls.data.update({"messages": [{"role": "user", "content": question}]})
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=cls.headers,
            json=cls.data,
        )
        reponse_data = response.json().get("choices")[0]["message"].get("content")
        return reponse_data
