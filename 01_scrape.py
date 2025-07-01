import requests
from bs4 import BeautifulSoup
import time
import csv
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
}

countries = [
    'france','allemagne', 'espagne', 'italie', 'belgique',
    'pays-bas', 'portugal', 'suede', 'autriche', 'irlande'
]

keywords = ['data', 'développeur']

def extract_offers(soup, country, keyword):
    offers_data = []
    offers = soup.find_all('li', id=lambda x: x and x.startswith('job-offer-'))
    for offer_li in offers:
        title = offer_li.find('h2', class_='cc-job-offer-title')
        title_text = title.get_text(strip=True) if title else 'N/A'

        company = offer_li.find('p', id=lambda x: x and 'company-name' in x)
        company_text = company.get_text(strip=True) if company else 'N/A'

        location_div = offer_li.find('div', id=lambda x: x and 'job-locations' in x)
        location = location_div.find('span').get_text(strip=True) if location_div else 'N/A'

        contract_div = offer_li.find('div', id=lambda x: x and 'contract-types' in x)
        contract = contract_div.find('span').get_text(strip=True) if contract_div else 'N/A'

        salary_span = offer_li.find('span', class_='cc-tag-primary-light')
        salary = salary_span.get_text(strip=True) if salary_span else 'N/A'

        offers_data.append({
            'Mot-clé': keyword,
            'Pays': country,
            'Titre': title_text,
            'Entreprise': company_text,
            'Lieu': location,
            'Contrat': contract,
            'Salaire': salary
        })
    return offers_data

all_offers = []

for keyword in keywords:
    for country in countries:
        print(f"\n=== Scraping: Mot-clé = {keyword} | Pays = {country} ===")
        page_num = 1
        while True:
            url = f'https://www.meteojob.com/jobs?what={keyword}&where={country}&page={page_num}'
            print(f"Scraping page {page_num}...")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_offers = extract_offers(soup, country, keyword)
                if not page_offers:
                    print("Aucune offre trouvée. Passage à la suite.")
                    break
                all_offers.extend(page_offers)
                page_num += 1
                time.sleep(random.uniform(2, 4)) 
            else:
                print(f"Erreur HTTP {response.status_code}. Fin du scraping pour cette combinaison.")
                break

print(f"\nTotal offres récupérées : {len(all_offers)}")


with open('offres_meteojob_multi_keywords.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Mot-clé', 'Pays', 'Titre', 'Entreprise', 'Lieu', 'Contrat', 'Salaire'])
    writer.writeheader()
    writer.writerows(all_offers)
