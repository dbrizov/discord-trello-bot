import os
import requests
import webhook_get

TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


def delete_webhook(webhook_id):
    requests.delete(
        f"https://api.trello.com/1/webhooks/{webhook_id}",
        params={
            "key": TRELLO_API_KEY,
            "token": TRELLO_TOKEN
        }
    )

    print(f"Delete webhook '{webhook_id}'")


if __name__ == "__main__":
    for webhook in webhook_get.get().json():
        webhook_id = webhook["id"]
        delete_webhook(webhook_id)
