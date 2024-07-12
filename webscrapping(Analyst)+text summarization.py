import requests
from bs4 import BeautifulSoup
import json

# Initialize lists to store scraped data
data = {}

# Set base URL and headers
base_url = 'https://theanalyst.com/eu/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

# Function to get the soup object
def get_soup(url, headers):
    response = requests.get(url, headers=headers)
    content = response.text
    return BeautifulSoup(content, 'lxml')

# Function to scrape the main page
def scrape_main_page(base_url, headers):
    soup = get_soup(base_url, headers)
    articles = soup.findAll('article', class_='teaser--has-image teaser-type--post teaser--lg teaser')
    
    for article in articles:
        try:
            article_content = article.find('div', class_='teaser-content-wrapper')

            headline = article_content.find('a', class_='teaser-content-link').text.strip()

            link = article_content.find('a')['href'][4:]
            url = base_url + link

            data[headline] = scrape_inner_page(url, headers)
        except Exception as e:
            print(f"Error processing article: {e}")

# Function to scrape the inner page of each article
def scrape_inner_page(url, headers):
    inner_soup = get_soup(url, headers)
    try:
        outer_div = inner_soup.find('article', class_='post post-type-post')

        img = outer_div.find('img', class_='post-hero-image')['src']

        category = outer_div.find('div', class_='post-pills').text.strip()

        content_div = outer_div.find('div', class_='post-content-wrapper')
        paragraphs = content_div.findAll('p')

        sub_heading = paragraphs[0].text

        description = ' '.join(p.text for p in paragraphs[1:-1])

        return {
            "Link": url,
            "Image": img,
            "Category": category,
            "Sub Heading": sub_heading,
            "News Description": description
        }
    except Exception as e:
        print(f"Error processing inner page: {e}")
        return {}

# Main execution
scrape_main_page(base_url, headers)

print(len(data['Ollie Watkins: Four Touches, One Goal, One Final']['News Description']))

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def summarization(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = summarization({
	"inputs": data['Ollie Watkins: Four Touches, One Goal, One Final']['News Description'],
    "parameters": {"max_length": 150, "min_length": 50, "do_sample": False}
})
print(output)#[0]['summary_text'])

