import os
import json
from unittest.mock import patch, Mock
import pytest
from src.client.asi_client import call_model, ASIClientError

# Provide a fake URL so requests.post is predictable
os.environ["ASICLOUD_INFERENCE_URL"] = "https://fake.local/infer"

def make_mock_response(status_code=200, json_data=None, text=""):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.text = text
    if json_data is not None:
        mock_resp.json.return_value = json_data
    else:
        mock_resp.json.side_effect = ValueError("No JSON")
    return mock_resp

@patch("src.client.asi_client.requests.post")
def test_call_model_success(mock_post):
    expected = {"result": "ok"}
    mock_post.return_value = make_mock_response(200, json_data=expected)
    out = call_model("hello")
    assert out == expected

@patch("src.client.asi_client.requests.post")
def test_call_model_http_error(mock_post):
    mock_post.return_value = make_mock_response(400, json_data={"error": "bad"})
    with pytest.raises(ASIClientError) as exc:
        call_model("bad")
    assert "Model returned HTTP 400" in str(exc.value)

@patch("src.client.asi_client.requests.post")
def test_call_model_invalid_json(mock_post):
    mock_post.return_value = make_mock_response(200, json_data=None, text="not json")
    with pytest.raises(ASIClientError):
        call_model("nojson")
