# main.py
from generic_search import generic_search
from detailed_queries import fetch_availability, fetch_pricing
from parse_data import insert_data
from datetime import datetime

def main():
    # Define keyword for search
    # keyword = "Arduino Uno"  # Replace with your search term in generic search

    # Step 1: Perform generic search
    search_results = generic_search()

    part_data = []
    for result in search_results:
        mpn = result['part']['mpn']
        part_name = result['part']['name']
        part_id = result['part']['id']
        manufacturer_name = result['part']['manufacturer']['name']
        manufacturer_id = result['part']['manufacturer']['id']

        # Step 2: Fetch availability
        total_availability = fetch_availability(mpn)

        # #Step 3: Fetch pricing
        pricing = fetch_pricing(mpn)

        seller_data = []
        for seller in pricing['sellers']: 
            
            # Extract all prices from the parts data
            prices = []
            for offer in seller['offers']:
                for price_entry in offer.get('prices', []):  # Default to empty list if 'prices' key is missing
                    prices.append({
                        "quantity": price_entry['quantity'],
                        "currency": price_entry['currency'],
                        "price": round(price_entry['price'],2),
                        "conversionRate": round(price_entry['conversionRate'],2),
                        "convertedCurrency": price_entry['convertedCurrency'],
                        "convertedPrice": round(price_entry['convertedPrice'],2),
                    })
            seller_data.append({
                "company_name": seller['company']['name'],
                "prices": prices
            })

        # Date stamp
        today = datetime.today().strftime('%Y-%m-%d')
        # today = "2025-01-08"

        # Consolidate data
        part_data.append({
            "keyword": "Arduino Uno",
            "mpn": mpn,
            "part_name": part_name,
            "part_id": part_id,
            "manufacturer_name": manufacturer_name,
            "manufacturer_id": manufacturer_id,
            "total_availability": total_availability,
            "seller_data": seller_data,
            "date": today
        })


    db_data = insert_data(part_data)
    print(db_data)

if __name__ == "__main__":
    main()