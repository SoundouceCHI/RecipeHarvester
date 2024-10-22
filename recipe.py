class Recipe: 
    def __init__(self, title, nb_star, description, prep_time, cook_time, servings, ingredients_list, direction,calories, fat, carbs, protein) -> None:
        self.title = title
        self.nb_star=nb_star
        self.description = description
        self.prep_time = prep_time
        self.cook_time= cook_time
        self.servings= servings
        self.ingredients_list= ingredients_list
        self.direction = direction 
        self.calories = calories 
        self.fat = fat 
        self.carbs = carbs 
        self.protein = protein 

    def __str__(self) -> str:
        return f"""{self.title} :  {self.nb_star} etoiles. temps : {self.prep_time} / {self.cook_time} / {self.servings}  
                calories : {self.calories}, fat: {self.fat}, carbs: {self.carbs}, protein : {self.protein}
                description : {self.description} 
                ingredients : 
                  {self.ingredients_list}
                direction : 
                  {self.direction}
                """