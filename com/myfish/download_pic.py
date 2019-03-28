detail_url = "https://burst.shopify.com/photos/braving-the-cold-weather-running-in-ottawa"
from  selenium import webdriver

option = webdriver.Chrome()
option.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=option)
browser.get(detail_url)
print(browser.page_source)