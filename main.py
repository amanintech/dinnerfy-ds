from fastapi import FastAPI, Request, HTTPException
import uvicorn, json, pandas as pd

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/recipe")
async def get_recipe(request: Request):
    body = await request.body()

    try:
        json_body = json.loads(body)
        recipe_id = json_body['RecipeID']
        number_of_servings = json_body['Servings']
    except:
        raise HTTPException(status_code=400, 
                            detail={"required_fields" : ["RecipeID", "Servings"]})

    df = pd.read_csv("recipedata.csv")
    recipe = df[df['RecipeID'] == recipe_id]

    if recipe.empty:
        raise HTTPException(status_code=404, 
                            detail="The recipe with the provided RecipeID could not be found.")

    if f'Serves_{number_of_servings}' not in recipe.columns:
        raise HTTPException(status_code=404, 
                            detail="The recipe you requested does not have instructions available for the specified number of servings.")

    recipe = recipe[["RecipeID", "Name", "Recipe_Meta", "Interest_Tags", "Diet_Tags", "Cooking_Meta", f"Serves_{number_of_servings}"]]
    response = recipe.iloc[0].to_dict()
    return response