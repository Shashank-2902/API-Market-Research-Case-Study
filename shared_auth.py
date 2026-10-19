"""Nexar API authentication."""

import os

import requests

TOKEN_URL = "https://identity.nexar.com/connect/token"


def get_access_token():
    """Request an access token using the NEXAR_CLIENT_ID and NEXAR_CLIENT_SECRET variables."""
    client_id = os.getenv("NEXAR_CLIENT_ID")
    client_secret = os.getenv("NEXAR_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Set NEXAR_CLIENT_ID and NEXAR_CLIENT_SECRET before running.")

    response = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "supply.domain",
    })
    if response.status_code != 200:
        raise RuntimeError(f"Failed to retrieve token: {response.status_code}, {response.text}")
    return response.json().get("access_token")
