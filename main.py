from recipe_scrapper import Recipe_scrapper

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
recipe_scp = Recipe_scrapper('chicken')
recipe_scp.collect_recipes()
r = recipe_scp.get_recipe()
recipe_scp.close()