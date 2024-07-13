import requests
from bs4 import BeautifulSoup
import json

previous_news=[#'Twenty-Six and Counting: Spanish Teams’ Extraordinary Record in Finals',
#'Spain Weaknesses: Where England Could Hurt Euro 2024’s Best Team', 
'Spain vs England Prediction: Euro 2024 Final Match Preview', 
'The Quiet Maestro: How Fabián Ruiz is Dominating Midfield at Euro 2024',
'Euro 2024’s Most Resilient Side, England Can Fight Their Way to Glory',
'Ollie Watkins: Four Touches, One Goal, One Final',
'Netherlands 1-2 England Stats: Super Sub Watkins Fires Three Lions Into Euro 2024 Final', 
'Uruguay 0-1 Colombia Stats: Dogged Cafeteros Dig in to Reach Copa America Final',
'Changing Seas: The NBA Winners and Losers of the 2024 Offseason',
'Is Harry Kane a Problem for England, or Just a Quieter Solution?',
'Eight of the Best Players Still Available on a Free Transfer in 2024']

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

import re

def filter_string(s):
    match = re.search(r'2.*', s)
    if match:
        return match.group()
    return None

# Example usage
single_string = "/eu/2024/07/spanish-teams-extraordinary-record-in-finals-26-wins/"


# Function to scrape the main page
def scrape_main_page(base_url, headers):
    soup = get_soup(base_url, headers)
    articles = soup.findAll('article', class_='teaser--has-image teaser-type--post teaser--lg teaser')
    
    for article in articles:
        try:
            article_content = article.find('div', class_='teaser-content-wrapper')

            headline = article_content.find('a', class_='teaser-content-link').text.strip()
            #print(headline)
            link = article_content.find('a')['href']
            link = filter_string(link)
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


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}
# 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
def summarization(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
x=list(data.keys())
for i in x:
    if i in previous_news:
        continue
    dis=data[i]['News Description'][:1020]
    previous_news.append(i)# appending current news to database
    output = summarization({
        "inputs": dis,
        "parameters": {"max_length": 350, "min_length": 50, "do_sample": False}
    })
    print('Link',data[i]['Link'])
    print('Image',data[i]['Image'])
    print('category',data[i]['Category'])
    print('sub_heading',data[i]['Sub Heading'])
    print('Heading',i)
    print(output)#[0]['summary_text'])

