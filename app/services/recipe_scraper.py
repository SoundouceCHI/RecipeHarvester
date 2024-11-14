from selenium import webdriver 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db.recipe_db import Recipe
from utils import is_recipe

class Recipe_scraper():

    BASE_URL = 'https://www.allrecipes.com'
    recipes_links = []
    def __init__(self,search_mode,keyword=""):
        self.keyword = keyword
        self.init_research(search_mode)
        self._init_driver()

    def init_research(self, search_mode): 
        if search_mode == 1: 
            self.page_url= f'{self.BASE_URL}/search?q={self.keyword}'
        else: 
            self.page_url = self.BASE_URL

    def _init_driver(self):        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def collect_recipes(self, input_choice):
        page_url = self.page_url
        self.driver.get(page_url)
        selector = 'a[id^="mntl-card-list-items"]' if input_choice == 2 else 'a[id^="mntl-card-list-card--extendable"]'
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="onetrust-reject-all-handler"]'))).click()
        for e in self.driver.find_elements(By.CSS_SELECTOR,selector):
            self.recipes_links.append(
                {
                    'title' : e.find_element(By.CSS_SELECTOR,'.card__title-text').text,
                    'url' : e.get_attribute('href')
                }
            )
        # print(self.recipes_links)
    
    @classmethod
    def get_only_recipes(cls):
        cls.recipes_links = [recipe for recipe in cls.recipes_links if recipe.get('url') and is_recipe(recipe.get('url'))]
        return cls.recipes_links
    
    def get_recipe_obj(self, url): 
        self.driver.get(url)
        if is_recipe(url) :  
            recipe = {
                'title': self.driver.find_element(By.TAG_NAME, 'h1').text, 
                'nb_star': self.driver.find_element(By.CSS_SELECTOR, '#mm-recipes-review-bar__rating_1-0').text, 
                'description': self.driver.find_element(By.CSS_SELECTOR, ".article-subheading.text-body-100").text,
                'info_prep': self.__extract_info_prep(), 
                'ingredients_list': [i.text for i in self.driver.find_element(By.CLASS_NAME, 'mm-recipes-structured-ingredients__list').find_elements(By.TAG_NAME, "p")], 
                'direction': [i.text for i in self.driver.find_element(By.ID, 'mm-recipes-steps__content_1-0').find_elements(By.CSS_SELECTOR,'li > p')],
                'nutrition_fact': self.__extract_nutrition_fct()
            }

            return recipe
    
    def __extract_info_prep(self) -> dict: 
        infos = self.driver.find_elements(By.CSS_SELECTOR, '.mm-recipes-details__value') 
        return {['prep_time', 'cook_time', 'total_time', 'additional_time','servings','yield'][i]: infos[i].text for i in range(len(infos))}
    
    def __extract_nutrition_fct(self) -> dict: 
        infos = self.driver.find_elements(By.CSS_SELECTOR, '.mm-recipes-details__value') 
        return {['prep_time', 'cook_time', 'total_time', 'additional_time','servings','yield'][i]: infos[i].text for i in range(len(infos))}

    def collect_recipe_by_idx(self, idx): 
        page_url = self.recipes_links[idx].get('url') 
        return page_url         

    def get_idx_of_recipe(self, recipe_title) -> int : 
        for index, recipe in enumerate(self.recipes_links):
            if recipe['title'] == recipe_title:
                return index
        # print(f"Recipe titled '{recipe_title}' not found.")
        return -1

    def get_recipe(self,recipe_title): 
        idx = self.get_idx_of_recipe(recipe_title)
        if idx != -1 : 
            page_url = self.collect_recipe_by_idx(idx) 
            recipe_obj = self.get_recipe_obj(page_url)
            if recipe_obj:
                recipe = Recipe(recipe_obj.get('title'), recipe_obj.get('nb_star'), 
                                recipe_obj.get('description'), recipe_obj.get('info_prep').get('prep_time'), 
                                recipe_obj.get('info_prep').get('cook_time'), recipe_obj.get('info_prep').get('servings'),
                                recipe_obj.get('ingredients_list'), recipe_obj.get('direction'), 
                                recipe_obj.get('nutrition_fact').get('calories'), recipe_obj.get('nutrition_fact').get('fat'), 
                                recipe_obj.get('nutrition_fact').get('carbs'), recipe_obj.get('nutrition_fact').get('protein')
                                )
                # print(recipe)
                return recipe
        
    def close(self): 
        self.driver.quit() 
    
    @classmethod
    def scrape_recipes(cls): 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        user_input = int(input("""
                            1. Cherchez une recette 
                            2. Recette tendance 
        """))
        if user_input == 1: 
            recipe_scp = Recipe_scraper(user_input,'chicken')
            recipe_scp.collect_recipes(1)
            # r = recipe_scp.get_recipe("Chicken Fried Chicken")
        else : 
            recipe_scp = Recipe_scraper(user_input)
            recipe_scp.collect_recipes(2)    
        only_recipes = Recipe_scraper.get_only_recipes()
        recipe_scp.close()

        return only_recipes