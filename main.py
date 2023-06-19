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
    
    return json_body


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="localhost", port=5000)