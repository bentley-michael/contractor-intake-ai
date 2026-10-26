"""Webhook tests for examples/sample-intake-workflow.json.

These tests send real HTTP requests to a running n8n instance that has the
sample workflow imported and published. They skip when nothing is listening,
so a plain `pytest` run does not fail on a machine without n8n.

Environment variables:
  WEBHOOK_URL     default http://127.0.0.1:5678/webhook/sample-intake
  WEBHOOK_SECRET  default REPLACE_WITH_A_LONG_RANDOM_SECRET, the placeholder
                  in the sample workflow
"""
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

URL = os.environ.get("WEBHOOK_URL", "http://127.0.0.1:5678/webhook/sample-intake")
SECRET = os.environ.get("WEBHOOK_SECRET", "REPLACE_WITH_A_LONG_RANDOM_SECRET")
EVENT = json.loads(
    (Path(__file__).parent.parent / "examples" / "sample-intake-event.json").read_text()
)


def post(body, secret=SECRET):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if secret is not None:
        headers["x-webhook-secret"] = secret
    req = urllib.request.Request(URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode()


def parsed(text):
    try:
        return json.loads(text)
    except ValueError:
        return {}


@pytest.fixture(scope="module", autouse=True)
def n8n_is_up():
    """Skip when nothing listens. Otherwise wait for the webhook to register.

    n8n answers its health check before it registers webhooks, so requests
    sent right after startup get a 404 for a short time.
    """
    deadline = time.time() + 60
    while True:
        try:
            status, _ = post({}, secret="probe")
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            pytest.skip(f"No n8n webhook listening at {URL}")
        if status != 404 or time.time() > deadline:
            return
        time.sleep(1)


def test_qualified_lead_is_routed_and_normalized():
    status, text = post(EVENT)
    out = parsed(text)
    assert status == 200, text
    assert out["route"] == "qualified"
    assert out["lead"]["phone"] == "+16155550142"
    assert out["lead"]["email"] == "jordan@example.com"


def test_sales_call_is_routed_as_junk():
    event = json.loads(json.dumps(EVENT))
    event["request"]["service"] = ""
    event["request"]["summary"] = "Robocall about an extended warranty."
    status, text = post(event)
    out = parsed(text)
    assert status == 200, text
    assert out["route"] == "junk"
    assert out["reason"]


def test_missing_event_id_is_invalid():
    event = json.loads(json.dumps(EVENT))
    del event["event_id"]
    status, text = post(event)
    out = parsed(text)
    assert status == 400, text
    assert out["route"] == "invalid"
    assert out["error"]


def test_wrong_secret_is_rejected():
    status, text = post(EVENT, secret="not-the-secret")
    assert status == 401, text


def test_missing_secret_is_rejected():
    status, text = post(EVENT, secret=None)
    assert status == 401, text


def test_empty_body_is_rejected():
    status, text = post(None)
    assert status == 400, text
