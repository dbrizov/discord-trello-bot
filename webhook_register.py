import os
import requests

TRELLO_BOARD_ID = "69c91c2f99b08f4c8ab31b06"
TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


def register():
    response = requests.post("https://api.trello.com/1/webhooks", data={
        "callbackURL": "https://placeholder/trello-webhook",
        "idModel": TRELLO_BOARD_ID,
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    })

    return response


if __name__ == "__main__":
    response = register()
    print(response.status_code)
    print(response.text)
