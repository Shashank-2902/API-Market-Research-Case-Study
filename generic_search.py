"""Searches the Nexar API for the parts matching the search keyword."""

import requests

import shared_auth

API_URL = "https://api.nexar.com/graphql"
SEARCH_KEYWORD = "Arduino Uno"
RESULT_LIMIT = 1

QUERY = """
query partSearch {
  supSearch(q: "%s", limit: %d) {
    hits
    results {
      part {
        id
        name
        mpn
        manufacturer {
          id
          name
        }
      }
    }
  }
}
"""


def generic_search():
    """Return the list of search results for SEARCH_KEYWORD."""
    headers = {
        "Authorization": f"Bearer {shared_auth.get_access_token()}",
        "Content-Type": "application/json",
    }
    payload = {"query": QUERY % (SEARCH_KEYWORD, RESULT_LIMIT)}
    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"GraphQL error: {response.status_code}, {response.text}")
    return response.json()["data"]["supSearch"]["results"]
