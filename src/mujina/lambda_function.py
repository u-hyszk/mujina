import json
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def respond(err, res=None):
    ret = {
        "statusCode": "200",
        "body": json.dumps(res, ensure_ascii=False),
        "headers": {
            "Content-Type": "application/json",
        },
    }
    LOGGER.info(f"Return: {ret}")
    return ret


def lambda_handler(event, context):
    LOGGER.info(f"Received event: {json.dumps(event)}")
    payload = {}
    if event.get("body"):
        payload = event["body"]
    return respond(None, payload)
