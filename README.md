# RecipeHarvester

RecipeHarvester is a web scraping tool designed to extract recipes from **Allrecipes** using Selenium. This project allows to access trending recipes from the homepage and perform recipe searches based on a keyword.

## Features

1. **Trending Recipes Scraping:**
   - RecipeHarvester can display trending recipes directly from Allrecipes’ homepage.

2. **Keyword-Based Search:**
   - Enter a keyword to search for specific recipes.
   - A test is implemented to verify if a page contains an ingredients list, ensuring that the page is indeed a recipe.

3. **Classes and Data Structures:**
   - **RecipeScraper**: the main class using Selenium to navigate and extract recipes from Allrecipes.
   - **Recipe**: a class to store recipe details, making data manipulation easier.

## Current Limitations

- **Limited to Allrecipes**: the scraper currently only works on this website.
- **Filtering Non-Recipe Articles**: some articles instead of recipes may still be fetched, which can cause scraping issues.

## Next Steps

- **Expansion to Other Sites**: plan to add support for additional recipe sites.
