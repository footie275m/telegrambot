from bs4 import BeautifulSoup
import json
HEADLINE=[]
LINK=[]
IMG=[]
CATEGORY=[]
SUB_HEADING=[]
NEWS_DESCRIPTION=[]
base_url = 'https://theanalyst.com/eu/'
headers={'User-Agent':'Mozilla/5.0(Windows NT 6.3; Win64; x64) AppleWebKit 537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
response = requests.get(base_url,headers=headers)
content = response.text
soup = BeautifulSoup(content,'lxml') 
articles = soup.findAll('article', class_='teaser--has-image teaser-type--post teaser--lg teaser')
for i in articles:
    article=i.find('div', class_='teaser-content-wrapper')

    headline=article.find('a', class_='teaser-content-link')
    headline=headline.text
    HEADLINE.append(headline)
    link=article.find('a')['href']
    link=link[4:]
    url=base_url+link
    LINK.append(url)
    response_inner_page = requests.get(url,headers=headers)
    inner_content = response_inner_page.text
    inner_soup = BeautifulSoup(inner_content,'lxml') 
    outer_div_test = inner_soup.find('article', class_='post post-type-post')
    img=outer_div_test.find('img', class_='post-hero-image')['src']
    IMG.append(img)
    category=outer_div_test.find('div', class_='post-pills').text
    CATEGORY.append(category)
    content=outer_div_test.find('div', class_='post-content-wrapper')
    content=content.findAll('p')
    n=len(content)
    des=[]
    for i in range(len(content)):
        if i==0:
            SUB_HEADING.append(content[i].text)
            continue
        if i ==(n-1):
            continue
        des.append(content[i].text)
    NEWS_DESCRIPTION.append(des)
    
