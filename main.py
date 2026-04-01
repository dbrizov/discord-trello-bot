import os
import flask
import requests
import discord_webhook

app = flask.Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")


@app.route("/trello-webhook", methods=["HEAD"])
def verify():
    return "", 200


@app.route("/trello-webhook", methods=["POST"])
def trello_event():
    data = flask.request.json
    are_env_vars_valid = DISCORD_WEBHOOK_URL and TRELLO_API_KEY and TRELLO_TOKEN
    if not data or not are_env_vars_valid:
        return "", 200

    action = data.get("action", {})
    action_type = action.get("type")
    member = action.get("memberCreator", {}).get("fullName", "Someone")
    card = action.get("data", {}).get("card", {}).get("name", "a card")
    list_name = action.get("data", {}).get("list", {}).get("name", "")
    list_after = action.get("data", {}).get("listAfter", {}).get("name")
    comment = action.get("data", {}).get("text", "")

    message = None
    webhook = None

    if action_type == "createCard":
        message = f"📋 **{member}** created card **{card}** in *{list_name}*"
        webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)  # type: ignore
    elif action_type == "commentCard":
        message = f"💬 **{member}** commented on **{card}**: {comment}"
        webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)  # type: ignore
    elif action_type == "updateCard" and list_after:
        message = f"🔄 **{member}** moved **{card}** to *{list_after}*"
        webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)  # type: ignore
    elif action_type == "addAttachmentToCard":
        attachment = action.get("data", {}).get("attachment", {})
        attachment_name = attachment.get("name", "a file")
        attachment_url = attachment.get("url", "")
        is_image = attachment_url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))

        if is_image:
            message = f"🖼️ **{member}** attached an image **{attachment_name}** to **{card}**"
            webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)  # type: ignore

            # Download the image and send it as a file
            image_response = requests.get(
                attachment_url,
                headers={
                    "Authorization": f'OAuth oauth_consumer_key="{TRELLO_API_KEY}", oauth_token="{TRELLO_TOKEN}"'
                }
            )

            webhook.add_file(file=image_response.content, filename=attachment_name)
        else:
            message = f"📎 **{member}** attached a file **{attachment_name}** to **{card}**\n{attachment_url}"
            webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)  # type: ignore

    if webhook:
        print(message)
        webhook.execute()

    return "", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
