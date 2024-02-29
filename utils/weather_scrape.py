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
#========asynchronous version =================== not working yet
# import asyncio
# import aiohttp
# import requests
# from bs4 import BeautifulSoup
# from django.http import JsonResponse

# async def scraped_data():
#     try:
#         url = "https://www.meteoblue.com/en/weather/week/bucegi-mountains_romania_683598"

#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 response.raise_for_status()  # Raise exception for bad response status codes
#                 html_content = await response.text()

#         soup = BeautifulSoup(html_content, 'html.parser')

#         temperature_element = soup.find("div", class_='current-temp')
#         picture_element = soup.find("span", class_='current-picto').find("img", src=True)['src']
#         description_element = soup.find("div", class_='current-description')

#         if not all([temperature_element, picture_element, description_element]):
#             raise ValueError("Required data not found on the website")

#         temperature = temperature_element.get_text(strip=True)[:10].strip()
#         description = description_element.get_text(strip=True)[:8]

#         # Return the scraped data as a dictionary
#         return {'temperature': temperature, 'picture': picture_element, 'description': description}

#     except (aiohttp.ClientError, ValueError, IndexError) as e:
#         return {'error': str(e)}