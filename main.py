from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import json
app = FastAPI()

class Request(BaseModel):
    RecipeID: int
    Servings: int


def find_recipe(dat,id,serves):
    if (id not in dat["RecipeID"].values)and ("Serves_"+str(serves) not in dat.columns):
        return {
    "Error":"One or More Entries are Invalid",
    "RecipeID": "Invalid",
    "Servings": "Invalid"
    } 
    if ("Serves_"+str(serves) not in dat.columns):
        return {
    "Error":"One or More Entries are Invalid",
    "RecipeID": id,
    "Servings": "Invalid"
    }
    elif (id not in dat["RecipeID"].values):
        return {
    "Error":"One or More Entries are Invalid",
    "RecipeID": "Invalid",
    "Servings": serves
    }
    
    item=dat.loc[dat["RecipeID"]==id]
    serve=item["Serves_"+str(serves)]
    js={
    "RecipeID":int(item["RecipeID"][id-1]),
    "Name":item["Name"][id-1],
    "Recipe_Meta":json.loads(item["Recipe_Meta"][id-1]),
    "Interest_Tags":json.loads(item["Interest_Tags"][id-1]),
    "Diet_Tags":json.loads(item["Diet_Tags"][id-1]),
    "Cooking_Meta":json.loads(item["Cooking_Meta"][id-1]),
    "Serve_"+str(serves):json.loads(serve[id-1])
}
    return js

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/recipe")
async def get_recipe(request: Request):
    data=pd.read_csv('recipedata.csv')
    res=find_recipe(data,request.RecipeID,request.Servings)
    return res