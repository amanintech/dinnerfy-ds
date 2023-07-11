from fastapi import FastAPI

from pydantic import BaseModel
import pandas as pd

import json


app = FastAPI()


class Request(BaseModel):
    RecipeID: int
    Servings: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/recipe")
def get_recipe(request: Request):
    data = pd.read_csv("./recipedata.csv")

    RecipeID = request.RecipeID

    if RecipeID not in data["RecipeID"].values:
        return {
            "Error": "Invalid RecipeID",
        }

    row = data[data["RecipeID"] == RecipeID]

    index = f"Serves_{request.Servings}"

    if index not in row:
        return {
            "Error": "Invalid Servings",
        }

    required_data = ["RecipeID", "Name", "Recipe_Meta", "Interest_Tags", "Diet_Tags", "Cooking_Meta", index]
    data = {}
    for col in required_data:
        curr_data = row[col][RecipeID-1]
        try:
            data[col] = int(curr_data)
        except:
            try:
                data[col] = json.loads(curr_data)
            except:
                data[col] = curr_data

    return data