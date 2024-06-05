import json
import logging
import os
import re

import requests

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def respond(res=None):
    ret = {
        "statusCode": "200",
        "body": json.dumps(res, ensure_ascii=False),
        "headers": {
            "Content-Type": "application/json",
        },
    }
    LOGGER.info(f"Return: {ret}")
    return ret


def post_message_to_slack(channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {os.environ.get('SlackBotUserOAuthToken')}",
    }
    data = {
        "token": os.environ.get("SlackVerificationToken"),
        "text": message,
        "channel": channel,
    }
    LOGGER.info(f"Header: {headers} Data: {data}")
    res = requests.post(url, data=json.dumps(data).encode("utf-8"), headers=headers)
    LOGGER.info(f"status: {res.status_code} content: {res.content}")


def get_message_from_slack(event):
    text = event["event"]["text"]  # 投稿されたテキスト全体を取得
    message = re.sub(r"<@.*?>", "", text)  # メンションを削除
    return message


def get_channel_from_slack(event):
    return event["event"]["channel"]


def lambda_handler(event, context):
    # 受信データをCloudWatchに出力
    LOGGER.info(f"Received event: {json.dumps(event)}")

    # Slack APIの認証
    if "challenge" in event:
        return event["challenge"]

    try:
        # オウム返し
        message = get_message_from_slack(event)
        channel = get_channel_from_slack(event)
    except Exception as e:
        LOGGER.error("get_messages failed")
        LOGGER.error(f"Error: {e}")
        return respond("Error")
    try:
        post_message_to_slack(channel, message)
    except Exception as e:
        LOGGER.error("post_message failed")
        LOGGER.error(f"Error: {e}")
        return respond("Error")

    return respond("OK")
