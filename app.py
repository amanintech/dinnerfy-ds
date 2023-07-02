from fastapi import FastAPI, Request
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI(title="dinnerfy")

# Reading the 'recipedata.csv' file
df = pd.read_csv('recipedata.csv')

# Function to extract image URL from the web
def extract_image_url(recipe_name):
    # Replace spaces in the recipe name with '%20' for the URL
    query = recipe_name.replace(' ', '%20')

    # Send a request to a search engine (e.g., Google) and parse the response
    response = requests.get(f"https://www.google.com/search?q={query}&tbm=isch")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the URL of the first image result
    image_url = soup.find('img')['src']

    return image_url

# Function to process recipe metadata
def process_recipe_meta(recipe_meta):
    # Replace '\n' with a newline character
    recipe_meta = recipe_meta.replace('\\n', '\n')

    # Remove backslash if it's present inside double quotes
    recipe_meta = recipe_meta.replace('\\"', '"')

    # Replace remaining backslashes with newline character
    recipe_meta = recipe_meta.replace('\\', '\n')

    return recipe_meta

# Route for the root endpoint
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# Route for the /hello/{name} endpoint
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

# Route for the /recipe endpoint
@app.post("/recipe")
async def get_recipe(recipe_id: int, serving: int):
    # Finding the recipe with the given recipe_id
    recipe = df[df['RecipeID'] == recipe_id].iloc[0]

    # Creating a dictionary to store the recipe information
    recipe_dict = {
        "RecipeID": int(recipe['RecipeID']),
        "Name": recipe['Name'],
        "image_url": extract_image_url(recipe['Name']),
        "themeColor": "null",
        "RecordID": recipe['RecordID'],
        "creatorID": "Dinnerfy",
        "Recipe_Meta": json.loads(process_recipe_meta(recipe['Recipe_Meta'])),
        "interest_tags": recipe['Interest_Tags'],
        "diet_tags": recipe['Diet_Tags'],
        "ingredients": recipe['ingredients'].split(','),
        "instructions": recipe['Cooking_Meta'].split('\n'),
        "servings": serving,
        "prepTime": recipe['Execution_Time'],
        "cookTime": recipe['Execution_Time']
    }

    return recipe_dict
