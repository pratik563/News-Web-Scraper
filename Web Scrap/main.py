import requests
from bs4 import BeautifulSoup
import csv

# fetch and parse a webpage
def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)  
        response.raise_for_status() 
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

# URL of the page to scrape
url = 'https://timesofindia.indiatimes.com/news'

# Fetch and parse the webpage
soup = fetch_page(url)
if soup:
    # Scrape data if the page is successfully fetched
    articles = soup.find_all('a', class_='VeCXM')  # Class may differ

    # Prepare data for CSV
    data = []
    for article in articles:
        headline = article.find('p', class_='CRKrj')
        headline_text = headline.text.strip() if headline else 'N/A'
        
        link = article['href']
        full_link = link if link.startswith('http') else f"https://timesofindia.indiatimes.com{link}"
        
        summary = article.find('p', class_='W4Hjm')
        summary_text = summary.text.strip() if summary else 'N/A'
        
        data.append([headline_text, full_link, summary_text])

    # Save to CSV
    with open('times_of_india_articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Headline', 'URL', 'Summary'])
        writer.writerows(data)

    print("Data successfully saved to times_of_india_articles.csv")
else:
    print("Failed to fetch the webpage.")
