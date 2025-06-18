import requests
from bs4 import BeautifulSoup
import time
from scraper.data_processing import parse_details
from scraper.database_utils import save_to_database

BASE_DOMAIN = "https://tulieuvankien.dangcongsan.vn"


def get_khoa_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    #all links for khoa section
    khoa_links = []
    #for link in soup.select('a[href*="/ban-chap-hanh-trung-uong-dang/bo-chinh-tri/khoa-"]'):
    for link in soup.select('a[href*="/ban-chap-hanh-trung-uong-dang/bo-chinh-tri/khoa-"], a[href*="/ban-chap-hanh-trung-uong-dang/ban-bi-thu/khoa-"]'):
        href = link.get('href')
        if href and 'khoa' in href:
            full_url = BASE_DOMAIN + href
            khoa_links.append(full_url)

        return khoa_links


#find links to individuals pages within each khoa
def get_person_links(khoa_url):
    response = requests.get(khoa_url)
    soup = BeautifulSoup(response.text, "html.parser")

    person_links = []
    for link in soup.select('a[href*="dong-chi"]'):
        href = link.get('href')
        if href:
            full_url = BASE_DOMAIN + href
            person_links.append(full_url)

    return person_links


#Extract Specific Information on Each Person’s Page
def scrape_person_content(person_url):
    response = requests.get(person_url)
    soup = BeautifulSoup(response.text, "html.parser")

    title_text = soup.title.get_text(strip=True)
    name = title_text.split('|')[0].strip()

    ring_smaller = soup.select_one('h1').get_text(strip=True)
    ring_larger = title_text.split('|')[1].strip() if '|' in title_text else None

    paragraphs = soup.find_all('p')
    details_text = "\n".join([p.get_text(strip=True) for p in paragraphs]) if paragraphs else None

    details = parse_details(details_text) if details_text else {}
    return {
        'url': person_url,
        'name': name,
        'ring_smaller': ring_smaller,
        'ring_larger': ring_larger,
        "details": details
    }


#Combine All Functions to Scrape All Individuals in Each "Khoa"
def scrape_all_khoa_data(base_url):
    all_data = []

    # Step 1: Get all khoa links
    khoa_links = get_khoa_links(base_url)

    # Step 2: For each khoa, get individual person links
    for khoa_url in khoa_links:
        person_links = get_person_links(khoa_url)

        # Step 3: For each person, scrape their information
        for person_url in person_links:
            person_data = scrape_person_content(person_url)
            if person_data:
                all_data.append(person_data)
                save_to_database(person_data)

            time.sleep(1)

    return all_data
