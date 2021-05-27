import re
import sys
from urllib.parse import urljoin

import bs4
import requests


def scrap(argv):
    """
    Giving argument, extract downloadable links
    :param argv: first: URL (string)
                second: Link name filter(regex)
                third: regex apply to href
    :return: Return list of downloadable links on sys.stdout
    """
    if len(argv) > 1:
        output = ""
        base_url = argv[1]
        # Get request, parse, and filter only hyperlinks.
        response = requests.get(base_url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        em_box = soup.find_all("a", href=True)
        # for each link
        for link in em_box:
            if len(argv) > 2:
              # If a second argument if provided (filter)
              if len(argv) > 3:
                temp = link.get("href")
              else:
                temp = link.text
              if re.match(argv[2].replace("?", "\xe9"), temp):
                  output += urljoin(base_url, link.get("href")) + "\n"
            else:
                output += urljoin(base_url, link.get("href")) + "\n"
        return output
    else:
        print("provide an valid url")
        return None

if __name__ == '__main__':
    print(scrap(sys.argv))