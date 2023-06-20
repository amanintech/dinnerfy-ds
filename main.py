from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_csv("recipedata.csv")

@app.post("/recipe/{recipe_id}")
def get_recipe(recipe_id: int, servings: int):
    recipe = df.iloc[recipe_id - 1]  # Access the row by recipe_id
    recipe_data = {
        "RecipeID": int(recipe['RecipeID']),
        "Name": recipe['Name'],
        "imageURL": "https://v5.airtableusercontent.com/v1/18/18/1687168800000/4wJVgFTbwCCDZ7BGgx8EvA/_YLzI_KX6Mgt7DKoHqjeWIIBwxM3K78JRJQtok7wmXrFEDOjAti7OxuWJ2se7oKzept4arxev2peHYPt4aPcAPZqCTnVcUuc3_Yy65z6ESjbA7POgzfQ-RsrHBFpy-jzD0t89ti89D-sJniA_jjclE5rgCEeX9wuUajKWnBg3ffG7tsxdavvVEQbXEKpYG3zCyiUxySBDHKLiIeIR52BuA/_0gBU9fD7dKSEYmEwEU2ePLsu9thGFIX2ZWU88ejUNQ",
        "themeColor": "null",
        "RecordID": "rec504vwu2cAuhahw",
        "creatorID": "Dinnerfy",
        "Recipe_Meta": recipe['Recipe_Meta'],
        "Interest_Tags": recipe['Interest_Tags'],
        "Diet_Tags": recipe['Diet_Tags'],
        "Cooking_Meta": recipe['Cooking_Meta'],
        f"Serves_{servings}": recipe[f"Serves_{servings}"]
    }
    return recipe_data