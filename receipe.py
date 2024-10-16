from selenium import webdriver 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



keyword = "zucchini"
nb= 1
page_url = f'https://www.allrecipes.com/search?{keyword}={keyword}&offset={nb}&q={keyword}'.format(keyword=keyword, nb=nb)
elements = []
url= "https://www.allrecipes.com/"
print("Fetching URL:", page_url)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(page_url)

titles =  [element.get_attribute('data-tag') for element in driver.find_elements(By.CLASS_NAME, "card__content ")]
recipe_links = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, 'a.comp.mntl-card-list-items.mntl-document-card.mntl-card.card.card--no-image')]



print(titles)

driver.quit()