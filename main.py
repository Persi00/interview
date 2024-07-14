import json, math

def readJsonFile(path):
    jsonFile = open(path, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

def getRecipiesThatMakeCertainItem(recipes : dict) -> dict:
    recipesThatMakeItem : dict = {}
    for recipeName in recipes:
        for result in recipes[recipeName]["results"]:
            if result["name"] not in recipesThatMakeItem:
                recipesThatMakeItem[result["name"]] = recipeName
                
    return recipesThatMakeItem

def generateGraphOfRecipes(product : str, recipes : dict, recipesThatMakeItem : dict) -> tuple[list, list]:
    graph : list = [[]]
    usedRecipes : dict = {}
    usedRecipes[ recipesThatMakeItem[product] ] = 0
    vertexsRecipe = [ {"name": recipesThatMakeItem[product], "amountBeingUsed": 0, "resultsOfRecipieBeingUsed": []} ]
    dfsStack = [0]

    while len(dfsStack) > 0:
        v = dfsStack.pop()
        ingredients = recipes[vertexsRecipe[v]["name"]]["ingredients"]
        for ingredient in ingredients:
            ingredientName = ingredient["name"]

            if ingredientName in recipesThatMakeItem:
                recipeName = recipesThatMakeItem[ingredientName]
                u = 0
                if recipeName not in usedRecipes:
                    u = len(usedRecipes)
                    usedRecipes[recipeName] = u
                    vertexsRecipe.append({"name": recipeName, "amountBeingUsed": 0, "resultsOfRecipieBeingUsed": [0] * len(recipes[recipeName]["results"])})
                    graph.append([])
                    dfsStack.append(u)
                else:
                    u = usedRecipes[recipeName]

                graph[v].append(u)

    return (graph, vertexsRecipe)

     
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

def getUsedMachines(product : str, productAmount : int, graph : list, vertexsRecipe : list, verticiesInTopologicalOrder : list, recipes : dict, extractors : dict) -> dict:
    for result in recipes[vertexsRecipe[0]["name"]]["results"]:
        if result["name"] == product:
            vertexsRecipe[0]["amountBeingUsed"] = productAmount / result["amount"]

    resources : dict = {}
    for v in verticiesInTopologicalOrder:
        recipeName = vertexsRecipe[v]["name"]
        recipeUsesCount = vertexsRecipe[v]["amountBeingUsed"]

        for ingredient in recipes[recipeName]["ingredients"]:
            ingredientName = ingredient["name"]
            ingredientAmount = ingredient["amount"]

            breakLoop = False
            for u in graph[v]:
                ingredientRecipeName = vertexsRecipe[u]["name"]
                ingredientRecipeUsesCount = vertexsRecipe[u]["amountBeingUsed"]
                usedOutput = vertexsRecipe[u]["resultsOfRecipieBeingUsed"]
                
                for i, result in enumerate(recipes[ingredientRecipeName]["results"]):
                    resultName = result["name"]
                    producedAmount = result["amount"]
                        
                    if resultName == ingredientName:
                        ingredientRecipeCycles = max(0, (ingredientAmount * recipeUsesCount - (producedAmount * ingredientRecipeUsesCount - usedOutput[i])) / producedAmount)
                        vertexsRecipe[u]["amountBeingUsed"] += ingredientRecipeCycles
                        vertexsRecipe[u]["resultsOfRecipieBeingUsed"][i] += ingredientAmount * recipeUsesCount

                        breakLoop = True
                        break

                if breakLoop:
                    break

            if not breakLoop:
                if ingredientName not in resources:
                    resources[ingredientName] = 0
                resources[ingredientName] += ingredientAmount * recipeUsesCount

    machines : dict = {}
    for resourceName in resources:
        extractorName = extractors[resourceName]["name"]
        amoutPerSecond = extractors[resourceName]["amount"]
        if extractorName not in machines:
            machines[extractorName] = 0

        machines[extractorName] += math.ceil(resources[resourceName] / amoutPerSecond)

    for recipe in vertexsRecipe:
        recipeName = recipe["name"]
        recipeUsesCount = recipe["amountBeingUsed"]
        machineName = recipes[recipeName]["machine"]["name"]
        machineSpeed = recipes[recipeName]["machine"]["speed"]
        duration = recipes[recipeName]["duration"]

        if machineName not in machines:
            machines[machineName] = 0
        machines[machineName] += math.ceil(recipeUsesCount * duration / machineSpeed)
        
    return machines

def getNeededMachines(product, productAmountPerSecond, mode = "normal"):
    recipes = readJsonFile(f"data/{mode}.json")
    extractors = readJsonFile("data/extractors.json")

    recipesThatMakeItem = getRecipiesThatMakeCertainItem(recipes)

    if not product in recipesThatMakeItem:
        raise ValueError("There is no recipe that makes such an item.") 

    graph, vertexsRecipe = generateGraphOfRecipes(product, recipes, recipesThatMakeItem)

    verticiesInTopologicalOrder = getVerticiesInTopologicalOrder(graph)

    return getUsedMachines(product, productAmountPerSecond, graph, vertexsRecipe, verticiesInTopologicalOrder, recipes, extractors)

if __name__ == "__main__":
    product = "plastic-bar"
    amountPerSecond = 1
    mode = "normal" 
    # mode = "expensive"
    machines = getNeededMachines(product, amountPerSecond, mode)

    print("Machines: ")
    for key in machines:
        print(f"{key}: {machines[key]}")