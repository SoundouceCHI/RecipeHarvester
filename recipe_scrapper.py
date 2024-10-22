from selenium import webdriver 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from recipe import Recipe

class Recipe_scrapper():

    BASE_URL = f'https://www.allrecipes.com/search?'
    recipes_links = []
    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.driver = self._init_driver()
        self.page_url = f'{self.BASE_URL}?{self.keyword}={self.keyword}&offset=1&q={self.keyword}'
        self._init_driver()
        
    def _init_driver(self):        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def collect_recipes(self):
        page_url = self.page_url
        self.driver.get(page_url)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="onetrust-reject-all-handler"]'))).click()
        for e in self.driver.find_elements(By.CSS_SELECTOR,'a[id^="mntl-card-list-items"]'):
            self.recipes_links.append(
                {
                    'title' : e.find_element(By.CSS_SELECTOR,'.card__title-text').text,
                    'url' : e.get_attribute('href')
                }
            )
        print(self.recipes_links)
    
    def get_recipe_obj(self, url) -> str: 
        self.driver.get(url)
        recipe = {
            'title': self.driver.find_element(By.TAG_NAME, 'h1').text, 
            'nb_star': self.driver.find_element(By.CSS_SELECTOR, '#mm-recipes-review-bar__rating_1-0').text, 
            'description': self.driver.find_element(By.CSS_SELECTOR, ".article-subheading.type--dog").text
        }

        infos = self.driver.find_elements(By.CSS_SELECTOR, '.mm-recipes-details__value') 
        recipe['info_prep'] = {['prep_time', 'cook_time', 'total_time', 'servings','yield'][i]: infos[i].text for i in range(len(infos))}

        recipe['ingredients_list'] = [i.text for i in self.driver.find_element(By.CLASS_NAME, 'mm-recipes-structured-ingredients__list').find_elements(By.TAG_NAME, "p")]

        recipe['direction']= [i.text for i in self.driver.find_element(By.ID, 'mm-recipes-steps__content_1-0').find_elements(By.CSS_SELECTOR,'li > p')]

        nutrition_fact = self.driver.find_elements(By.CLASS_NAME , 'mm-recipes-nutrition-facts-summary__table-cell.type--dog-bold')
        recipe['nutrition_fact'] = {['calories', 'fat', 'carbs','protein'][i]: nutrition_fact[i].text for i in range(len(nutrition_fact))}

        return recipe
    
    def collect_recipe_by_idx(self, idx): 
        page_url = self.recipes_links[idx].get('url') 
        return page_url 
        

    def get_idx_of_recipe(self, recipe_title) -> int : 
        try: 
            self.recipes_links.index(recipe_title)
        except:
            print("erreur")

    def get_recipe(self): 
        page_url = self.collect_recipe_by_idx(0) #change idx to a modifiable value 
        recipe_obj = self.get_recipe_obj(page_url)
        
        recipe = Recipe(recipe_obj.get('title'), recipe_obj.get('nb_star'), 
                        recipe_obj.get('description'), recipe_obj.get('info_prep').get('prep_time'), 
                        recipe_obj.get('info_prep').get('cook_time'), recipe_obj.get('info_prep').get('servings'),
                        recipe_obj.get('ingredients_list'), recipe_obj.get('direction'), 
                        recipe_obj.get('nutrition_fact').get('calories'), recipe_obj.get('nutrition_fact').get('fat'), 
                        recipe_obj.get('nutrition_fact').get('carbs'), recipe_obj.get('nutrition_fact').get('protein')
                        )
        print(recipe)
        return recipe
    
    def close(self): 
        self.driver.quit() 