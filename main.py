import json, math

def readJsonFile(path):
    jsonFile = open(path, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

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

def getUsedMachines(product, resultAmount, graph : list, vertexRecipe : list, verticiesInTopologicalOrder : list, recipes : dict) -> dict:
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
                
            machines["Electric mining drill"] += math.ceil(resources[resourceName] / 0.25)

        elif resourceName == "water":
            if not "Offshore pump" in machines:
                machines["Offshore pump"] = 0
            
            machines["Offshore pump"] += math.ceil(resources[resourceName] / 1200)

        elif resourceName == "crude-oil":
            if not "Pumpjack" in machines:
                machines["Pumpjack"] = 0
            
            machines["Pumpjack"] += math.ceil(resources[resourceName] / 10)

        else:
            if not "Electric mining drill" in machines:
                machines["Electric mining drill"] = 0
                
            machines["Electric mining drill"] += math.ceil(resources[resourceName] / 0.5)

    for recipe in vertexRecipe:
        recipeName, recipeUsesCount = recipe[0:2]
        machineName = recipes[recipeName]["machine"]["name"]
        machineSpeed = recipes[recipeName]["machine"]["speed"]
        duration = recipes[recipeName]["duration"]

        if not machineName in machines:
            machines[machineName] = 0
        machines[machineName] += math.ceil(recipeUsesCount * duration / machineSpeed)
        
    return machines

def getNeededMachines(product, resultAmount, mode = "normal"):
    recipes = readJsonFile(f"data/{mode}.json")

    whichRecipeToGet = mapItemsToRecipes(recipes)

    graph, vertexRecipe = generateGraphOfRecipes(product, recipes, whichRecipeToGet)

    verticiesInTopologicalOrder = getVerticiesInTopologicalOrder(graph)

    return getUsedMachines(product, resultAmount, graph, vertexRecipe, verticiesInTopologicalOrder, recipes)

if __name__ == "__main__":
    product = "iron-plate"
    amount = 1
    mode = "normal" 
    # mode = "expensive"
    machines = getNeededMachines(product, amount, mode)

    print("Machines: ")
    for key in machines:
        print(f"{key}: {machines[key]}")