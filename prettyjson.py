import json
import collections.abc

def readJsonFile(path):
    jsonFile = open(path, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

def formatIngredients(ingredients : list) -> list:
    formattedIngredients = []
    for ingred in ingredients:
        if isinstance(ingred, collections.abc.Sequence):
            formattedIngredients.append({"name": ingred[0], "amount": ingred[1]})
        else:
            formattedIngredients.append({"name": ingred["name"], "amount": ingred["amount"]})
    return formattedIngredients

def extractRecipes(recipesJson : list, machines: dict, mode : str = "normal") -> dict:
    recipes = {}

    for recipeJson in recipesJson:
        name = recipeJson["name"]
        recipes[name] = {}

        category = "crafting"
        if "category" in recipeJson:
            category = recipeJson["category"]

        recipes[name]["machine"] = machines[category]


        recipe = {}
        if mode in recipeJson:
            recipe = recipeJson[mode]
        else:
            recipe = recipeJson

        recipes[name]["ingredients"] = formatIngredients(recipe["ingredients"])

        recipes[name]["duration"] = 0.5
        if "energy_required" in recipe:
            recipes[name]["duration"] = recipe["energy_required"]
                
        if "result" in recipe:
            result = recipe["result"]
            amount = 1

            if "result_count" in recipe:
                amount = recipe["result_count"]

            recipes[name]["results"] = [{"name": result, "amount": amount}]

        elif "results" in recipe:
            recipes[name]["results"] = []
            for resultobj in recipe["results"]:
                result = ""
                amount = 0
                if isinstance(resultobj, collections.abc.Sequence):
                    result = resultobj[0]
                    amount = resultobj[1]
                else:
                    result = resultobj["name"]
                    amount = resultobj["amount"]

                recipes[name]["results"].append({"name": result, "amount": amount})

    return recipes

def dumpJsonFile(path, jsonData):
    jsonFile = open(path, "w+")
    json.dump(jsonData, jsonFile)
    jsonFile.close()

def prettyJson(mode):
    jsonData = readJsonFile("recipe.json")
    machines = readJsonFile("machines.json")
    recipes = extractRecipes(jsonData, machines, mode)
    dumpJsonFile(f"{mode}.json", recipes)

mode = "normal"
# mode = "expensive"
prettyJson(mode)