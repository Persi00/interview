import json, math

def readJsonFile(path):
    jsonFile = open(path, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

def mapItemsToRecipes(recipes : dict) -> dict:
    whichRecipeToGet : dict = {}
    for recipeName in recipes:
        for result in recipes[recipeName]["results"]:
            if not result["name"] in whichRecipeToGet:
                whichRecipeToGet[result["name"]] = []
            
            whichRecipeToGet[result["name"]].append(recipeName)
                
    return whichRecipeToGet

def generateGraphOfRecipes(product : str, recipes : dict, whichRecipeToGet : dict) -> tuple:
    graph : list = [[]]
    usedRecipes = {}
    usedRecipes[ whichRecipeToGet[product][0] ] = 0
    vertexRecipes = [ {"name": whichRecipeToGet[product][0], "usesCount": 0, "resultsUsedAmount": []} ]
    dfsStack = [0]

    while len(dfsStack) > 0:
        v = dfsStack.pop()
        ingredients = recipes[vertexRecipes[v]["name"]]["ingredients"]
        for ingred in ingredients:
            ingredName = ingred["name"]

            if ingredName in whichRecipeToGet:
                recipeName = whichRecipeToGet[ingredName][0]
                u = 0
                if not recipeName in usedRecipes:
                    u = len(usedRecipes)
                    usedRecipes[recipeName] = u
                    vertexRecipes.append({"name": recipeName, "usesCount": 0, "resultsUsedAmount": [0] * len(recipes[recipeName]["results"])})
                    graph.append([])
                else:
                    u = usedRecipes[recipeName]

                graph[v].append(u)
                dfsStack.append(u)

    return (graph, vertexRecipes)

     
def TopologicalSort(v : int, graph : list, visited : list, verticiesInTopologicalOrder : list) -> None:
    for u in graph[v]:
        if not visited[u]: 
            visited[u] = True
            TopologicalSort(u, graph, visited, verticiesInTopologicalOrder)
    verticiesInTopologicalOrder.append(v)

def getVerticiesInTopologicalOrder(graph : list) -> list:
    visited = [False] * len(graph)
    visited[0] = True

    verticiesInTopologicalOrder : list = []
    TopologicalSort(0, graph, visited, verticiesInTopologicalOrder)

    verticiesInTopologicalOrder.reverse()

    return verticiesInTopologicalOrder

def getUsedMachines(product : str, resultAmount : int, graph : list, vertexRecipes : list, verticiesInTopologicalOrder : list, recipes : dict, extractors : dict) -> dict:
    for result in recipes[vertexRecipes[0]["name"]]["results"]:
        if result["name"] == product:
            vertexRecipes[0]["usesCount"] = math.ceil(resultAmount / result["amount"])

    resources = {}
    for v in verticiesInTopologicalOrder:
        recipeName = vertexRecipes[v]["name"]
        recipeUsesCount = vertexRecipes[v]["usesCount"]

        for ingred in recipes[recipeName]["ingredients"]:
            ingredName = ingred["name"]
            ingredAmount = ingred["amount"]

            breakLoop = False
            for u in graph[v]:
                ingredRecipeName = vertexRecipes[u]["name"]
                ingredRecipeUsesCount = vertexRecipes[u]["usesCount"]
                usedOutput = vertexRecipes[u]["resultsUsedAmount"]

                recipes[ingredRecipeName]["results"]
                
                for i, result in enumerate(recipes[ingredRecipeName]["results"]):
                    resultName = result["name"]
                    producedAmount = result["amount"]
                        
                    if resultName == ingredName:
                        ingredRecipeCycles = math.ceil(max(0, (ingredAmount * recipeUsesCount - (producedAmount * ingredRecipeUsesCount - usedOutput[i])) / producedAmount))
                        vertexRecipes[u]["usesCount"] += ingredRecipeCycles
                        vertexRecipes[u]["resultsUsedAmount"][i] += ingredAmount * recipeUsesCount

                        breakLoop = True
                        break

                if breakLoop:
                    break

            if not breakLoop:
                if not ingredName in resources:
                    resources[ingredName] = 0
                resources[ingredName] += ingredAmount * recipeUsesCount

    machines = {}
    for resourceName in resources:
        extractorName = extractors[resourceName]["name"]
        amoutPerSecond = extractors[resourceName]["amount"]
        if not extractorName in machines:
            machines[extractorName] = 0

        machines[extractorName] += math.ceil(resources[resourceName] / amoutPerSecond)

    for recipe in vertexRecipes:
        recipeName = recipe["name"]
        recipeUsesCount = recipe["usesCount"]
        machineName = recipes[recipeName]["machine"]["name"]
        machineSpeed = recipes[recipeName]["machine"]["speed"]
        duration = recipes[recipeName]["duration"]

        if not machineName in machines:
            machines[machineName] = 0
        machines[machineName] += math.ceil(recipeUsesCount * duration / machineSpeed)
        
    return machines

def getNeededMachines(product, resultAmount, mode = "normal"):
    recipes = readJsonFile(f"data/{mode}.json")
    extractors = readJsonFile("data/extractors.json")

    whichRecipeToGet = mapItemsToRecipes(recipes)

    graph, vertexRecipes = generateGraphOfRecipes(product, recipes, whichRecipeToGet)

    verticiesInTopologicalOrder = getVerticiesInTopologicalOrder(graph)

    return getUsedMachines(product, resultAmount, graph, vertexRecipes, verticiesInTopologicalOrder, recipes, extractors)

if __name__ == "__main__":
    product = "plastic-bar"
    amount = 1
    mode = "normal" 
    # mode = "expensive"
    machines = getNeededMachines(product, amount, mode)

    print("Machines: ")
    for key in machines:
        print(f"{key}: {machines[key]}")