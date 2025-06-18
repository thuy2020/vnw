import os
import django

# Set up Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vnw.settings')

# Initialize Django
django.setup()  # Make sure this is called before any Django-dependent import

# Confirm DJANGO_SETTINGS_MODULE and installed apps
print("DJANGO_SETTINGS_MODULE:", os.getenv('DJANGO_SETTINGS_MODULE'))
print("INSTALLED_APPS:", django.conf.settings.INSTALLED_APPS)  # Debug check


base_url = "https://tulieuvankien.dangcongsan.vn/ban-chap-hanh-trung-uong-dang/index"

if __name__ == "__main__":
    from scraper.scraper import scrape_all_khoa_data
    from scraper.database_utils import save_to_database

    data = scrape_all_khoa_data(base_url)

    if data:
        for person_data in data:
            print(f"Name: {person_data['name']}")
            print(f"Ring small: {person_data['ring_smaller']}")
            print(f"Ring large: {person_data['ring_larger']}")
            print(f"URL: {person_data['url']}")
            print(f"Details: {person_data['details']}")
            print("-" * 40)

            save_to_database(person_data)


    else:
        print("No data found.")
