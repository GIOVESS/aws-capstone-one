import base64
import json
import logging
import os
import uuid

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}


def _response(status: int, body: dict) -> dict:
    return {"statusCode": status, "headers": HEADERS, "body": json.dumps(body)}


def _parse_body(event: dict) -> dict:
    raw = event.get("body")
    if raw is None:
        raise ValueError("Request body is empty")
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object")
    return payload


def handler(event, context):
    request_id = getattr(context, "aws_request_id", "local")
    try:
        payload = _parse_body(event)
    except (ValueError, json.JSONDecodeError) as exc:
        logger.warning(json.dumps({"event": "invalid_request", "error": str(exc), "request_id": request_id}))
        return _response(400, {"message": f"Invalid request: {exc}"})

    try:
        submission_id = uuid.uuid4().hex[:8]
        logger.info(json.dumps({
            "event": "submission_received",
            "id": submission_id,
            "request_id": request_id,
            "payload": payload,
        }))
        return _response(200, {
            "message": "Data successfully received and logged!",
            "id": submission_id,
        })
    except Exception:
        logger.exception("Unhandled error")
        return _response(500, {"message": "Internal server error"})
