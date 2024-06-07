import json
import logging
import os
import re
from io import BytesIO

import requests
from pypdf import PdfReader

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


# 環境変数
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# APIのURL
SLACK_API_URL = "https://slack.com/api/"


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
    url = os.path.join(SLACK_API_URL, "chat.postMessage")
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    data = {
        "text": message,
        "channel": channel,
    }
    LOGGER.info(f"Header: {headers} Data: {data}")
    res = requests.post(url, headers=headers, data=json.dumps(data))
    res.raise_for_status()
    LOGGER.info(f"status: {res.status_code} content: {res.content}")
    return res.json()


def download_pdf(file_url):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    res = requests.get(file_url, headers=headers)
    res.raise_for_status()
    pdf_stream = BytesIO(res.content)
    return pdf_stream


def extract_text_from_pdf(pdf_stream):
    reader = PdfReader(pdf_stream)
    n_pages = len(reader.pages)
    texts = []
    for page_idx in range(n_pages):
        page = reader.pages[page_idx]
        page_text = page.extract_text()
        texts.append(page_text)
    return "".join(texts)


def extract_message_from_slack(event):
    text = event["event"]["text"]  # 投稿されたテキスト全体を取得
    message = re.sub(r"<@.*?>", "", text)  # メンションを削除
    return message


def extract_channel_from_slack(event):
    return event["event"]["channel"]


def extract_pdf_url_from_slack(event):
    if "files" in event["event"]:
        for file_info in event["event"]["files"]:
            if file_info["filetype"] == "pdf":
                return file_info["url_private"]
    return None


def lambda_handler(event, context):
    # 受信データをCloudWatchに出力
    LOGGER.info(f"Received event: {json.dumps(event)}")

    # Slack APIの認証
    if "challenge" in event:
        return event["challenge"]

    try:
        # オウム返し
        message = extract_message_from_slack(event)
        channel = extract_channel_from_slack(event)
        pdf_url = extract_pdf_url_from_slack(event)
        if pdf_url:
            pdf_stream = download_pdf(pdf_url)
            text = extract_text_from_pdf(pdf_stream)
            post_message_to_slack(channel, text)
        post_message_to_slack(channel, message)
    except Exception as e:
        LOGGER.error(f"Error: {e}")
        return respond("Error")

    return respond("OK")


# import os
# import json
# import requests
# import boto3
# from PyPDF2 import PdfFileReader
# from io import BytesIO

# SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

# def download_pdf(file_url):
#     headers = {
#         'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
#     }
#     response = requests.get(file_url, headers=headers)
#     response.raise_for_status()
#     return BytesIO(response.content)

# def extract_text_from_pdf(pdf_stream):
#     reader = PdfFileReader(pdf_stream)
#     text = ""
#     for page_num in range(reader.getNumPages()):
#         page = reader.getPage(page_num)
#         text += page.extractText()
#     return text

# def post_message_to_slack(channel, text):
#     url = 'https://slack.com/api/chat.postMessage'
#     headers = {
#         'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'channel': channel,
#         'text': text
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     response.raise_for_status()
#     return response.json()

# def lambda_handler(event, context):
#     body = json.loads(event['body'])

#     if 'event' in body and body['event']['type'] == 'app_mention':
#         event_data = body['event']
#         channel = event_data['channel']

#         if 'files' in event_data:
#             for file_info in event_data['files']:
#                 if file_info['filetype'] == 'pdf':
#                     file_url = file_info['url_private']
#                     pdf_stream = download_pdf(file_url)
#                     text = extract_text_from_pdf(pdf_stream)
#                     post_message_to_slack(channel, text)
#                     break

#     return {
#         'statusCode': 200,
#         'body': json.dumps('Success')
#     }
