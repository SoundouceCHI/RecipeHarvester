from selenium import webdriver 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Receipe_scrapper():

    BASE_URL = f'https://www.allrecipes.com/search?'
    receipes_links = []
    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.driver = self._init_driver()
        self.page_url = f'{self.BASE_URL}?{self.keyword}={self.keyword}&offset=1&q={self.keyword}'
        self._init_driver()
        
    def _init_driver(self):        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def collect_receipe(self):
        page_url = self.page_url
        self.driver.get(page_url)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="onetrust-reject-all-handler"]'))).click()
        for e in self.driver.find_elements(By.CSS_SELECTOR,'a[id^="mntl-card-list-items"]'):
            self.receipes_links.append(
                {
                    'title' : e.find_element(By.CSS_SELECTOR,'.card__title-text').text,
                    'url' : e.get_attribute('href')
                }
            )
        print(self.receipes_links)
    
    def close(self): 
        self.driver.quit() 