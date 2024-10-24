from recipe_scrapper import Recipe_scrapper

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
user_input = int(input("""
                    1. Cherchez une recette 
                    2. Recette tendance 
"""))
if user_input == 1: 
    recipe_scp = Recipe_scrapper(user_input,'chicken')
    recipe_scp.collect_recipes()
    r = recipe_scp.get_recipe("Chicken Fried Chicken")

else : 
    recipe_scp = Recipe_scrapper(user_input)
    recipe_scp.collect_recipes()

    
recipe_scp.close()