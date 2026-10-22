"""Nexar GraphQL queries for one part: total availability and seller prices."""

import requests

from shared_auth import get_access_token

API_URL = "https://api.nexar.com/graphql"

AVAILABILITY_QUERY = """
query totalAvailability($mpn: String!) {
  supSearchMpn(q: $mpn, limit: 1) {
    results {
      description
      part {
        totalAvail
        mpn
      }
    }
  }
}
"""

PRICING_QUERY = """
query pricingByVolumeLevels($mpn: String!) {
  supSearchMpn(country: "DE", currency: "EUR", q: $mpn, limit: 1) {
    hits
    results {
      part {
        sellers {
          company {
            name
          }
          offers {
            prices {
              quantity
              price
              currency
              conversionRate
              convertedPrice
              convertedCurrency
            }
          }
        }
      }
    }
  }
}
"""


def _first_part(query, mpn):
    """Run a supSearchMpn query and return the first matching part."""
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
    }
    response = requests.post(API_URL, json={"query": query, "variables": {"mpn": mpn}}, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"GraphQL error: {response.status_code}, {response.text}")
    return response.json()["data"]["supSearchMpn"]["results"][0]["part"]


def fetch_availability(mpn):
    """Return the total quantity available across all sellers."""
    return _first_part(AVAILABILITY_QUERY, mpn)["totalAvail"]


def fetch_pricing(mpn):
    """Return the part with its sellers and their prices, converted to EUR."""
    return _first_part(PRICING_QUERY, mpn)
