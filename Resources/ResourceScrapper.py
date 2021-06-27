import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import service

def get_url(search_term):
    template = "https://www.amazon.in/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(' ','+')

    # adding page query to navigate to the next page.
    url = template.format(search_term)
    url += "&page={}"

    return url

# function to generate detailed info from the data
def extract_record(item):

    # getting description and url of the item
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.in" + atag.get('href')

    try:
        # getting the price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
        
    try:
        # getting the rating and review count
        rating = item.i.text
        review_count = item.find('span','a-size-base').text
    except:
        rating = 'N/A'
        review_count = 'N/A'

    # combining everything
    result = (description,price,rating,review_count,url)
    return result

def main(search_term):
    records = []
    # starting the webdriver.
    driver = webdriver.Chrome()
    url = get_url(search_term)

    for page in range(1,21):

        # navigating through all the pages
        driver.get(url.format(page))
        # extracting the data from website.
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type': 's-search-result'})
    
        for item in results:
            # appending each item's data to records list.
            record = extract_record(item)
            if record:
                records.append(record)
    
    driver.close()

    # writing the scrapped data to a csv file for analysis
    with open('resources.csv', 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Rating','Review Count','Url'])
        writer.writerows(records)
    print(records)

main('N95 Masks')