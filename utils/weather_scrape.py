import json
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup


def scraped_data():
    # Scrape data and store it in a variable called scraped_data
    url = "https://www.meteoblue.com/en/weather/week/bucegi-mountains_romania_683598"
    tag1 = "div"
    attr1 = 'class'
    attr_name1 = 'current-temp'
    tag2 = "span"
    attr2 = 'class'
    attr_name2 = 'current-picto'
    tag3 = "div"
    attr3 = 'class'
    attr_name3 = 'current-description'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    temp = soup.find_all(tag1, {attr1:attr_name1})[0].get_text().strip()[:10].strip()
    pic = soup.find_all(tag2, {attr2:attr_name2})[0].find_all("img", src=True)[0]['src']
    descr = soup.find_all(tag3, {attr3:attr_name3})[0].get_text().strip()[:8]
    # Convert the scraped data to a dictionary
    scraped_data_dict = {'temperature': temp, 'picture': pic, 'description': descr}
    # Return the scraped data as a JSON response
    return scraped_data_dict
