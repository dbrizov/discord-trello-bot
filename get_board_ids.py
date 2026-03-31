import os
import requests

TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


def get_board_ids():
    response = requests.get(
        "https://api.trello.com/1/members/me/boards",
        params={
            "key": TRELLO_API_KEY,
            "token": TRELLO_TOKEN
        }
    )

    return response


if __name__ == "__main__":
    response = get_board_ids()
    for board in response.json():
        print(board["name"], "->", board["id"])
