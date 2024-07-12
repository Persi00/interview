import json
import collections.abc
import math


product = "plastic-bar"
resultAmount = 1
mode = "normal" 
# mode = "expensive"

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

def mapItemsToRecipes(recipes : dict) -> dict:
    whichRecipeToGet = {}
    for name in recipes:
        for result in recipes[name]["results"]:
            if result["name"] in whichRecipeToGet: 
                whichRecipeToGet[result["name"]].append(name)
            else:
                whichRecipeToGet[result["name"]] = [name]
    return whichRecipeToGet

def generateGraphOfRecipes(product : str, recipes : dict, whichRecipeToGet : dict) -> tuple:
    graph = [[]]
    addedRecipes = {}
    addedRecipes[whichRecipeToGet[product][0]] = 0
    vertexRecipe = [ [whichRecipeToGet[product][0], 0, []] ]
    dfsStack = [0]
    while len(dfsStack):
        v = dfsStack.pop()
        ingredients = recipes[vertexRecipe[v][0]]["ingredients"]
        for ingred in ingredients:
            name = ingred["name"]

            if name in whichRecipeToGet:
                recipeName = whichRecipeToGet[name][0]
                u = 0
                if not recipeName in addedRecipes:
                    u = len(addedRecipes)
                    addedRecipes[recipeName] = u
                    vertexRecipe.append([recipeName, 0, [0] * len(recipes[recipeName]["results"])])
                    graph.append([])
                else:
                    u = addedRecipes[recipeName]

                graph[v].append(u)
                dfsStack.append(u)

    return (graph, vertexRecipe)

     
def TopologicalSort(v : int, graph : list, visited : list, verticiesInTopologicalOrder : list) -> None:
    for u in graph[v]:
        if not visited[u]: 
            visited[u] = True
            TopologicalSort(u, graph, visited, verticiesInTopologicalOrder)
    verticiesInTopologicalOrder.append(v)

def getVerticiesInTopologicalOrder(graph : list) -> list:
    visited = [False] * len(graph)
    visited[0] = True

    verticiesInTopologicalOrder = []
    TopologicalSort(0, graph, visited, verticiesInTopologicalOrder)

    verticiesInTopologicalOrder.reverse()

    return verticiesInTopologicalOrder

def getUsedResourcesAndMachines(product, resultAmount, graph : list, vertexRecipe : list, verticiesInTopologicalOrder : list, recipes : dict) -> dict:
    for result in recipes[vertexRecipe[0][0]]["results"]:
        if result["name"] == product:
            vertexRecipe[0][1] = math.ceil(resultAmount / result["amount"])

    resources = {}
    for v in verticiesInTopologicalOrder:
        recipeName, recipeUsesCount = vertexRecipe[v][0:2]
        for ingred in recipes[recipeName]["ingredients"]:
            name = ingred["name"]
            amount = ingred["amount"]

            breakLoop = False
            for u in graph[v]:
                ingredRecipeName, ingredRecipeUsesCount, usedOutput = vertexRecipe[u]
                
                for i, result in zip(range(len(recipes[ingredRecipeName]["results"])), recipes[ingredRecipeName]["results"]):
                    resultName = result["name"]
                    producedAmount = result["amount"]
                        
                    if resultName == name:
                        recipeCycles = math.ceil(max(0, (amount * recipeUsesCount - (producedAmount * ingredRecipeUsesCount - usedOutput[i])) / producedAmount))
                        vertexRecipe[u][1] += recipeCycles
                        vertexRecipe[u][2][i] += amount * recipeUsesCount

                        breakLoop = True
                        break

                if breakLoop:
                    break

            if not breakLoop:
                if not name in resources:
                    resources[name] = 0
                resources[name] += amount * recipeUsesCount

    machines = {}
    for resourceName in resources:
        if resourceName == "uranium-ore":
            if not "Electric mining drill" in machines:
                machines["Electric mining drill"] = 0
                
            machines["Electric mining drill"] += resources[resourceName] * 4

        elif resourceName == "water":
            if not "Offshore pump" in machines:
                machines["Offshore pump"] = 0
            
            machines["Offshore pump"] += math.ceil(resources[resourceName] / 1200)

        elif resourceName == "crude-oil":
            if not "Pumpjack" in machines:
                machines["Pumpjack"] = 0
            
            machines["Pumpjack"] += math.ceil(resources[resourceName] / 2)

        else:
            if not "Electric mining drill" in machines:
                machines["Electric mining drill"] = 0
                
            machines["Electric mining drill"] += resources[resourceName] * 2

    for recipe in vertexRecipe:
        recipeName, recipeUsesCount = recipe[0:2]
        machineName = recipes[recipeName]["machine"]
        duration = recipes[recipeName]["duration"]

        machinesCount = recipeUsesCount * duration

        if machineName == "Assembling machine 3":
            machinesCount /= 1.25

        elif machineName == "Electric furnace":
            machinesCount /= 2

        if not machineName in machines:
            machines[machineName] = 0
        machines[machineName] += math.ceil(machinesCount)
        
    return resources, machines

def getNeededResourcesAndMachines(product, resultAmount, mode = "normal"):
    recipesJson = readJsonFile("recipe.json")
    machinesJson = readJsonFile("machines.json")

    recipes = extractRecipes(recipesJson, machinesJson, mode)

    whichRecipeToGet = mapItemsToRecipes(recipes)

    graph, vertexRecipe = generateGraphOfRecipes(product, recipes, whichRecipeToGet)

    verticiesInTopologicalOrder = getVerticiesInTopologicalOrder(graph)

    return getUsedResourcesAndMachines(product, resultAmount, graph, vertexRecipe, verticiesInTopologicalOrder, recipes)


resources, machines = getNeededResourcesAndMachines(product, resultAmount, mode)

print("Resources: ")
for key in resources:
    print(f"{key}: {resources[key]} units")

print("\nMachines: ")
for key in machines:
    print(f"{key}: {machines[key]} units")