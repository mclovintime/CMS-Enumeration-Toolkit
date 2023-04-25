#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import unicodecsv as csv
import argparse

#usage syntax:
# python3 yellow_pages.py <keyword> <place ex: Regina,CA> <# of pages>


def parse_listing(keyword, place, page):
    """

    Function to process yellowpage listing page
    : param keyword: search query
    : param place : place name
    : param page : # of pages to query (there's typically 30 results to a page)

    """

    url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}&page={2}".format(keyword, place, page)

    print("retrieving ", url)

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'www.yellowpages.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
               }
    # Adding retries
    for retry in range(10):
        try:
            response = requests.get(url, verify=False, headers=headers)
            print("parsing page")
            if response.status_code == 200:
                parser = html.fromstring(response.text)
                
                base_url = "https://www.yellowpages.com"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = "//div[@class='search-results organic']//div[@class='v-card']"
                listings = parser.xpath(XPATH_LISTINGS)
                scraped_results = []

                for results in listings:
                    XPATH_BUSINESS_NAME = ".//a[@class='business-name']//text()"
                    XPATH_TELEPHONE = ".//div[@class='phones phone primary']//text()"
                    XPATH_WEBSITE = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href"
                   
                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)
                    raw_business_telephone = results.xpath(XPATH_TELEPHONE)
                    # raw_business_page = results.xpath(XPATH_BUSSINESS_PAGE)
                    # raw_categories = results.xpath(XPATH_CATEGORIES)
                    raw_website = results.xpath(XPATH_WEBSITE)
                    # raw_rating = results.xpath(XPATH_RATING)
                    # address = results.xpath(XPATH_ADDRESS)
                    # raw_street = results.xpath(XPATH_STREET)
                    # raw_locality = results.xpath(XPATH_LOCALITY)
                    # raw_region = results.xpath(XPATH_REGION)
                    # raw_zip_code = results.xpath(XPATH_ZIP_CODE)
                    # raw_rank = results.xpath(XPATH_RANK)

                    business_name = ''.join(raw_business_name).strip() if raw_business_name else None
                    telephone = ''.join(raw_business_telephone).strip() if raw_business_telephone else None
                    # business_page = ''.join(raw_business_page).strip() if raw_business_page else None
                    # rank = ''.join(raw_rank).replace('.\xa0', '') if raw_rank else None
                    # category = ','.join(raw_categories).strip() if raw_categories else None
                    website = ''.join(raw_website).strip() if raw_website else None
                    # rating = ''.join(raw_rating).replace("(", "").replace(")", "").strip() if raw_rating else None
                    # street = ''.join(raw_street).strip() if raw_street else None
                    # locality = ''.join(raw_locality).replace(',\xa0', '').strip() if raw_locality else None
                    # locality, locality_parts = locality.split(',')
                    # _, region, zipcode = locality_parts.split(' ')

                    business_details = {
                        'business_name': business_name,
                        'telephone': telephone,
                        # 'business_page': business_page,
                        # 'rank': rank,
                        # 'category': category,
                        'website': website,
                        # 'rating': rating,
                        # 'street': street,
                        # 'locality': locality,
                        # 'region': region,
                        # 'zipcode': zipcode,
                        # 'listing_url': response.url
                    }
                    scraped_results.append(business_details)

                return scraped_results

            elif response.status_code == 404:
                print("Could not find a location matching", place)
                # no need to retry for non existing page
                break
            else:
                print("Failed to process page")
                return []

        except:
            print("Failed to process page")
            return []


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='Search Keyword')
    argparser.add_argument('place', help='Place Name')
    argparser.add_argument('pages_to_scrape', type=int, help='Number of pages to scrape')

    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place
    pages_to_scrape = args.pages_to_scrape

    scraped_data = []
    # scraped_data = parse_listing(keyword, place)

    for page in range(1, pages_to_scrape + 1):
        scraped_data.extend(parse_listing(keyword, place, page))

    if scraped_data:
        print("Writing scraped data to %s-%s-yellowpages-scraped-data.csv" % (keyword, place))
        with open('%s-%s-%spg.csv' % (keyword, place, pages_to_scrape), 'wb') as csvfile:
            # update fieldnames to include more fields in the output .csv
            fieldnames = ['business_name', 'telephone', 'website']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
