"""Collects part, availability and price data from the Nexar API into SQLite."""

from datetime import datetime

from detailed_queries import fetch_availability, fetch_pricing
from generic_search import SEARCH_KEYWORD, generic_search
from parse_data import insert_data


def extract_prices(seller):
    """Flatten all price entries of one seller across its offers."""
    prices = []
    for offer in seller["offers"]:
        for entry in offer.get("prices", []):
            prices.append({
                "quantity": entry["quantity"],
                "currency": entry["currency"],
                "price": round(entry["price"], 2),
                "conversionRate": round(entry["conversionRate"], 2),
                "convertedCurrency": entry["convertedCurrency"],
                "convertedPrice": round(entry["convertedPrice"], 2),
            })
    return prices


def collect_part(result, today):
    """Fetch availability and pricing for one search result and return a record."""
    part = result["part"]
    mpn = part["mpn"]

    pricing = fetch_pricing(mpn)
    seller_data = [
        {"company_name": seller["company"]["name"], "prices": extract_prices(seller)}
        for seller in pricing["sellers"]
    ]

    return {
        "keyword": SEARCH_KEYWORD,
        "mpn": mpn,
        "part_name": part["name"],
        "part_id": part["id"],
        "manufacturer_name": part["manufacturer"]["name"],
        "manufacturer_id": part["manufacturer"]["id"],
        "total_availability": fetch_availability(mpn),
        "seller_data": seller_data,
        "date": today,
    }


def main():
    today = datetime.today().strftime("%Y-%m-%d")
    part_data = [collect_part(result, today) for result in generic_search()]
    print(insert_data(part_data))


if __name__ == "__main__":
    main()
