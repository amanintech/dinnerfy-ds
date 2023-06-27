from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/recipe")
def get_recipe(request:dict):
    data = pd.read_csv('./recipedata.csv')
    row = data[data['RecipeID']==request["RecipeID"]]
    index =f'Serves_{request["Servings"]}'
    return {"Data":json.loads(row[index][0])}
