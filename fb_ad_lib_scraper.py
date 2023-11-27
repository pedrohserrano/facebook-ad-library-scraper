"""-----------------------------------------------------------------------------
  Name: FB_AD_LIB_SCRAPER (Facebook Ads Library Scraper)
  Description: It doesn't really scrapes, it actually makes API calls to the "Meta Ad Library API" - https://www.facebook.com/ads/library/api/ to extract Ads metadata based on a search term
  Created By:  Pedro V (p.hernandezserrano@maastrichtuniversity.nl) with the help of ChatGPT 4 and based on the original fork from Max Woolf https://github.com/minimaxir/facebook-ad-library-scraper
  Last Update: 27/11/23
-----------------------------------------------------------------------------"""

import yaml
import requests
import csv
import datetime
import sys
from tqdm import tqdm

# Function to make API requests
def make_api_request(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Request failed with status code {response.status_code}: {response.text}")

# Function to fetch all pages of data
def fetch_all_data(api_url, params, max_pages=10):
    all_data = []
    for _ in tqdm(range(max_pages), desc="Fetching data"):
        data = make_api_request(api_url, params)
        all_data.extend(data.get('data', []))
        
        next_page = data.get('paging', {}).get('next')
        if not next_page:
            break

        params['after'] = data['paging']['cursors']['after']

    return all_data

# -----------------------------------------------------------
# MAKING THE API CALL TO THE FACEBOOK ADS LIBRARY
# -----------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fb_ad_lib_scraper.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]

# Load configuration file (here is where the search parameters are set)
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# API parameters
api_url = f"https://graph.facebook.com/{config['api_version']}/ads_archive"
params = {
    'access_token': config['access_token'],
    'ad_type': config['ad_type'],
    'ad_reached_countries': config['ad_reached_countries'],
    'ad_active_status': config['ad_active_status'],
    'search_terms': search_term,
    'fields': ','.join(config['fields']),
    'limit': config['page_total']
}

# Fetch data
data = fetch_all_data(api_url, params, config['max_pages'])

# Write data to CSV
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/fb_ads_{timestamp}.csv"
with open(filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=config['fields'])
    writer.writeheader()
    for ad in data:
        writer.writerow(ad)
