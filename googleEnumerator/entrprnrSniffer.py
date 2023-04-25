# Google Places business enumeration
# usage: python3 entrprnrSniffer.py


import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

load_dotenv()

api_key = os.environ['SECRET_KEY']

# import search_type_list.py as search_type_list
from search_type_list import search_type_list

def get_coordinates(city, retries=3, timeout=5):
    geolocator = Nominatim(user_agent="city_locator", timeout=timeout)
    try:
        location = geolocator.geocode(city)
        if location:
            resolvedLocation = str(location.latitude)+","+str(location.longitude)
            return resolvedLocation
        else:
            return None
    except GeocoderTimedOut:
        if retries > 0:
            return get_coordinates(city, retries - 1)
        else:
            print("Geocoder timed out. Try again later fam.")
            return None
    except GeocoderServiceError as error:
        print(f"Error: {error}")
        return None


def get_local_business_websites(api_key, location, radius):
    business_websites = []
    for search_type in search_type_list:
        print("Checking search type ",search_type)
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={search_type}&key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            for result in data['results']:
                place_id = result['place_id']
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=website&key={api_key}"
                details_response = requests.get(details_url)

                if details_response.status_code == 200:
                    details_data = details_response.json()
                    if 'result' in details_data and 'website' in details_data['result']:
                        website = details_data['result']['website']
                        business_websites.append(website)
        else:
            print(f"Error fetching data from the Google Places API: {response.status_code}")

    return business_websites
    

def main():

    global api_key
    if not api_key:
        api_key = ""  # Replace with your Google Places API key

    location = get_coordinates(input("Enter city: "))
    dist = input("Enter radius in miles: ")
    radius = (float(dist) * 1.60934) 

    business_websites = get_local_business_websites(api_key, location, radius)

    print(f"Found {len(business_websites)} local business websites:")

    with open("googlePlacesResults.txt", 'w') as database:
        for website in business_websites:
            database.write(website + "\n")
            print(website)

if __name__ == '__main__':
    main()