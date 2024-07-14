import main
import pytest

@pytest.fixture
def recipes():
    return main.readJsonFile("data/normal.json")

@pytest.fixture
def recipesThatMakeItem(recipes):
    return main.getRecipiesThatMakeCertainItem(recipes)

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        (("iron-plate", 1, "normal"), {"Electric mining drill": 2, "Electric furnace": 2}),
        (("iron-gear-wheel", 2, "expensive"), {"Electric mining drill": 16, "Electric furnace": 13, "Assembling machine 3": 1}),
        (("uranium-235", 1, "normal"), {"Centrifuge": 1715, "Electric mining drill": 5715}),
        (("uranium-238", 1, "normal"), {"Centrifuge": 13, "Electric mining drill": 41}),
        (("uranium-238", 20, "normal"), {"Centrifuge": 242, "Electric mining drill": 806}),
        (("electronic-circuit", 1, "normal"), {"Electric mining drill": 5, "Electric furnace": 5, "Assembling machine 3": 2}),
        (("electronic-circuit", 2, "normal"), {"Electric mining drill": 10, "Electric furnace": 9, "Assembling machine 3": 3}),
        (("speed-module", 1, "normal"), {"Offshore pump": 1, "Electric mining drill": 105, "Pumpjack": 19, "Electric furnace": 76, "Oil refinery": 10, "Chemical plant": 5, "Assembling machine 3": 55}),
        (("rocket-part", 1, "normal"), {"Rocket silo": 3, "Electric mining drill": 3022, "Offshore pump": 2, "Pumpjack": 360, "Electric furnace": 2426, "Oil refinery": 180, "Chemical plant": 299, "Assembling machine 3": 1622})
    )
)
def test_getNeededMachines(input, expected):
    assert main.getNeededMachines(input[0], input[1], input[2]) == expected

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("copper-cable", [[1], []]),
        ("advanced-circuit", [[1, 2, 3], [3, 6], [5], [4], [], [], []]),
        ("pump", [[1, 2, 3], [2, 3, 5], [4], [4], [], [4]]),
        ("satellite", [[1, 2, 3, 4, 5, 6], [14, 16, 19], [9, 16, 19], [13, 18], [9, 13, 17], [9, 10, 11], [7, 8], [8], [], [13, 15], [9, 14, 15], [12, 13], [8], [], [8], [16], [], [13], [11, 13, 16], [13]])
    )
)
def test_generateGraphOfRecipes(input, expected, recipes, recipesThatMakeItem) :
    graph, vertexsRecipe = main.generateGraphOfRecipes(input, recipes, recipesThatMakeItem)
    for i in range(len(graph)):
        graph[i].sort()
    
    assert graph == expected

@pytest.mark.parametrize(
    ("graph"),
    (
        ([[]]),
        ([[1], []]),
        ([[1], [2], []]),
        ([[1, 2], [], []]),
        ([[2, 1], [3], [3], []]),
        ([[2, 4, 5], [], [3, 4], [], [5, 1], [1]])
    )
)
def test_getVerticiesInTopologicalOrder(graph):
    verticiesInTopologicalOrder = main.getVerticiesInTopologicalOrder(graph)
    transposed = [[] for _ in range(len(graph))]
    for v in range(len(graph)):
        for u in graph[v]:
            transposed[u].append(v)

    ok = True
    visited = [False] * len(graph)
    for v in verticiesInTopologicalOrder:
        processedPrevious = True
        for u in transposed[v]:
            if visited[u] == False:
                processedPrevious = False
                break

        if processedPrevious == False:
            ok = False
            break
        visited[v] = True
    assert ok