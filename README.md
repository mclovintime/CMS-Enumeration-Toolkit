# Content Management System Enumeration Toolkit (CMSET)
## by mclovintime, 2023

### Prerequisites

The program requires the following packages: 
 1. lxml
 2. requests

python -m pip install requests
sudo apt-get install python3-lxml

### Usage

This toolkit allows for the mass enumeration of content management systems (CMS) in use by websites within a given area
Freelance web developers can use this tool to identify potential clients who use clunky, outdated, or vulnerable site-builders/CMS
Here's a list of CMSs for reference: https://en.wikipedia.org/wiki/List_of_content_management_systems

The user can use their Google API key to collect websites with Google Places *WIP*
AND/OR
use the yellowpages webcrawler without any setup required (recommended)

### Operation Manual

1. Collect website lists from YPCrawler
    - cd YPEnumerator/yellowpages-scraper
    - python3 yellow_pages.py <keyword> <place ex: Regina,CA> <# of results pages to scan> 

    *results are usually 30 links per page*

2. Sanitize websites from collected .csv files (remove duplicates and format for scanning)
    - python3 sanitizer.py <input.csv> <input2.csv> ... <output.txt>
    - remember to save .csv files for a record of contact phone number if desired/available
    - copy sanitized.txt to the root folder

3. Scan for desired CMSs using spider.py
    - cd to root folder
    - in spider.py, add to the list "target_strings" any keywords from an HTML scan which would identify your targeted CMSs
        example: "wix", "elementor"
    - verify that the list you want scanned (sanitized.txt) is copied to the root folder
    - run with the following command: python3 spider.py
    - check CMSenumeration.txt to watch the results being written

Have fun!
