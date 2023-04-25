import random
import requests
from bs4 import BeautifulSoup

# CMS Enumaration Toolkit by McLovintime
# Anno Domini 2023
# I love you



sanitized_websites = []
element_placeholder = "DEFAULT CLASS"

def sites_sanitizer(input_file, output_file, blacklist):
    with open(input_file, 'r') as file:
        websites = file.readlines()

    for website in websites:
        if not any(word in website for word in blacklist):
            sanitized_websites.append(website.strip())

    with open(output_file, 'w') as file:
        for website in sanitized_websites:
            file.write(website + "\n")

    print(f"Filtered websites using blacklist tags from {input_file} written to {output_file}")

def main():
    input_file = "sanitized.txt"
    output_file = "filteredsites.txt"
    # fill the list below to exclude websites containing any of the tags
    blacklist = ["facebook", "uhaul", "jimmyjohns", "mcdonalds", "redroof", "walmart", "wellsfargo", "wellsfargodealerservices", "subway"]

    sites_sanitizer(input_file, output_file, blacklist)

if __name__ == '__main__':
    main()

def sniffCMS(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    ]
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # add more target strings from common classes below to find more CMSs
            # later I'll add a dictionary and save you from finding classes yourself
            target_strings = ["wix", "elementor"]

            target_classes = [
                tag['class']
                for tag in soup.find_all(attrs={'class': True})
                if any(target_string in cls for cls in tag['class'] for target_string in target_strings)
            ]

    
            if target_classes:
                element_placeholder = target_classes[0]

                for target_class in target_classes:
                    for target_string in target_strings:
                        if any(target_string in s for s in target_class):
                            element_placeholder = target_string
                            break
                    else:
                        continue
                    break

                return True, element_placeholder

    except requests.exceptions.RequestException as e:
        print(f"Error checking {url}: {e}")
        if isinstance(e, requests.exceptions.ConnectionError) and "RemoteDisconnected" in str(e):
            return True, "possibly_enfold"
    return False, None

def main():
    identified_sites = []
    with open("CMSenumeration.txt", "a") as f:
        for url in sanitized_websites:
            print(f"Checking {url}...")
            found_something, element_placeholder = sniffCMS(url)
            if found_something:
                identified_sites.append(url)
                f.write(url + " " + "class: " + element_placeholder + '\n')
                f.flush()  # flush the buffer and write to file immediately
                print(f"{url} uses contained targeted class {element_placeholder}.")
                print("~ we've nailed one! ~")

    print(f"\nFound {len(identified_sites)} websites using defined CMS:")

if __name__ == '__main__':
    main()