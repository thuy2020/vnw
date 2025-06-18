from django.shortcuts import render
from .scraper import scrape_all_khoa_data
import time


def scrape_view(request):
    base_url = "https://tulieuvankien.dangcongsan.vn/ban-chap-hanh-trung-uong-dang/index"
    scraped_data = scrape_all_khoa_data(base_url)

    return render(request, 'scraper/scrape_result.html', {'scraped_data': scraped_data})

