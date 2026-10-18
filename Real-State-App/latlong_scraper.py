
import requests
import pandas as pd
import time
from pathlib import Path

# Nominatim geocoding API
BASE_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "RealEstatePricePredictor/1.0 (personal research project)"
}

def get_coordinates(sector):
    params = {
        "q": f"Sector {sector}, Gurugram, Haryana, India",
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in",
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=HEADERS,
            timeout=20
        )
        response.raise_for_status()
        results = response.json()

        if results:
            result = results[0]
            return {
                "Latitude": float(result["lat"]),
                "Longitude": float(result["lon"]),
                "Matched Location": result["display_name"],
                "Status": "Found"
            }

        return {
            "Latitude": None,
            "Longitude": None,
            "Matched Location": None,
            "Status": "Not found"
        }

    except requests.RequestException as error:
        print(f"Sector {sector}: {error}")
        return {
            "Latitude": None,
            "Longitude": None,
            "Matched Location": None,
            "Status": "Request failed"
        }

# Collect results
records = []

for sector in range(1, 116):
    print(f"Fetching Sector {sector}...")

    result = get_coordinates(sector)

    records.append({
        "Sector": f"Sector {sector}",
        **result
    })

    # Respect the public API's usage policy
    time.sleep(1.1)

# Create DataFrame
df = pd.DataFrame(records)

# Save CSV relative to this script's working directory
output_path = Path("../DATA/Featured_Data/gurgaon_sectors_coordinates_latlong.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} records to: {output_path.resolve()}")
print(df.head())
print("\nStatus summary:")
print(df["Status"].value_counts())
