from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()


df = pd.read_csv("./recipedata.csv")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/recipe/{recipe_id}/{no_of_serve}")
async def get_recipe(recipe_id: int, no_of_serve: int):

    if recipe_id not in df["RecipeID"].values:
        raise HTTPException(status_code=404, detail="Recipe for the given RecipeID not found")
    
    if f"Serves_{no_of_serve}" not in df.columns:
        raise HTTPException(status_code=404, detail="Recipe for the given number of serve not found")
    
    recipe = df[["RecipeID", "Name", "Recipe_Meta", "Interest_Tags", "Diet_Tags", "Cooking_Meta", f"Serves_{no_of_serve}"]]
    recipe = recipe[recipe['RecipeID'] == recipe_id].to_dict('records')[0]

    return recipe
    