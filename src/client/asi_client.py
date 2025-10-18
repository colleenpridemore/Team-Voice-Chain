#!/usr/bin/env python3
"""
Minimal example client for calling an ASICloud-hosted model (asi1-mini).
Confirm the exact request/response schema with ASICloud docs before production use.
"""
from __future__ import annotations
import os
import requests
from typing import Any, Dict

DEFAULT_URL = "https://asicloud.cudos.org/inference/models/asi1-mini"
DEFAULT_TIMEOUT = 30

class ASIClientError(Exception):
    pass

def get_headers() -> Dict[str, str]:
    api_key = os.environ.get("ASICLOUD_API_KEY")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers

def call_model(payload: Any, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    Send payload to the ASICloud inference endpoint.

    Note: The request body below uses {"input": ...} as a placeholder.
    Verify the exact schema required by ASICloud for asi1-mini and update accordingly.
    """
    url = os.environ.get("ASICLOUD_INFERENCE_URL", DEFAULT_URL)
    headers = get_headers()
    body = {"input": payload}

    try:
        resp = requests.post(url, json=body, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise ASIClientError(f"Request failed: {e}") from e

    if resp.status_code >= 400:
        # Try to include server error message
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise ASIClientError(f"Model returned HTTP {resp.status_code}: {detail}")

    try:
        return resp.json()
    except ValueError:
        raise ASIClientError("Failed to parse JSON response from model")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Call ASI1-mini model (CLI)")
    parser.add_argument("--text", required=True, help="Text to send to the model")
    args = parser.parse_args()

    try:
        out = call_model(args.text)
        print("Model response:", out)
    except Exception as e:
        print("Error:", e)
        raise
