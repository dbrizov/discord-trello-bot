import os
import requests

TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


def get():
    response = requests.get(
        f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks",
        params={
            "key": TRELLO_API_KEY,
            "token": TRELLO_TOKEN
        }
    )

    return response


if __name__ == "__main__":
    response = get()
    print(response.status_code)
    print(response.text)
