"""-----------------------------------------------------------------------------
  Name: FB_AD_LIB_SCRAPER (Facebook Ads Library Scraper)
  Description: It doesn't really scrapes, it actually makes API calls to the "Meta Ad Library API" - https://www.facebook.com/ads/library/api/ to extract Ads metadata based on a search term
  Created By:  Pedro V (p.hernandezserrano@maastrichtuniversity.nl) with the help of ChatGPT 4 and based on the original fork from Max Woolf https://github.com/minimaxir/facebook-ad-library-scraper
  Last Update: 27/11/23
-----------------------------------------------------------------------------"""

import csv
import json
import datetime
import sys

def process_ad_data(input_file):
    # Timestamp for output file names
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Output file names
    demographic_output_file = f"data/fb_ads_demographic_{timestamp}.csv"
    region_output_file = f"data/fb_ads_region_{timestamp}.csv"

    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Preparing to write demographic distribution data
        with open(demographic_output_file, 'w', newline='', encoding='utf-8') as demofile:
            demo_fieldnames = ['ad_id', 'age', 'gender', 'percentage']
            demo_writer = csv.DictWriter(demofile, fieldnames=demo_fieldnames)
            demo_writer.writeheader()

            # Preparing to write region distribution data
            with open(region_output_file, 'w', newline='', encoding='utf-8') as regionfile:
                region_fieldnames = ['ad_id', 'region', 'percentage']
                region_writer = csv.DictWriter(regionfile, fieldnames=region_fieldnames)
                region_writer.writeheader()

                for row in reader:
                    ad_id = row['id']

                    # Process demographic distribution
                    if row['demographic_distribution']:
                        demographics = json.loads(row['demographic_distribution'].replace("'", '"'))
                        for demo in demographics:
                            demo_data = {
                                'ad_id': ad_id,
                                'age': demo['age'],
                                'gender': demo['gender'],
                                'percentage': demo['percentage']
                            }
                            demo_writer.writerow(demo_data)

                    # Process region distribution
                    if row['delivery_by_region']:
                        try: 
                            regions = json.loads(row['delivery_by_region'].replace("'", '"'))
                            for region in regions:
                                region_data = {
                                    'ad_id': ad_id,
                                    'region': region['region'],
                                    'percentage': region['percentage']
                                }
                                region_writer.writerow(region_data)
                        except json.JSONDecodeError as e:
                            #print(f"Error parsing JSON for ad_id {ad_id}: {row['delivery_by_region']}")
                            print(f"JSON error (Skipping): {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fb_ads_demographics_and_regions.py <input_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    process_ad_data(input_file_path)