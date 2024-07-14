import main
import pytest

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        (("iron-plate", 1), {'Electric mining drill': 2, "Electric furnace": 2}),
        (("uranium-235", 1), {'Centrifuge': 1715, 'Electric mining drill': 5715}),
        (("uranium-238", 1), {'Centrifuge': 13, 'Electric mining drill': 41}),
        (("uranium-238", 20), {'Centrifuge': 242, 'Electric mining drill': 806}),
        (("electronic-circuit", 1), {'Electric mining drill': 5, "Electric furnace": 5, "Assembling machine 3": 2}),
        (("electronic-circuit", 2), {'Electric mining drill': 10, "Electric furnace": 9, "Assembling machine 3": 3}),
        (("speed-module", 1), {"Offshore pump": 1, "Electric mining drill": 105, "Pumpjack": 19, "Electric furnace": 76, "Oil refinery": 10, "Chemical plant": 5, "Assembling machine 3": 55}),
        (("rocket-part", 1), {"Rocket silo": 3, "Electric mining drill": 3022, "Offshore pump": 2, "Pumpjack": 360, "Electric furnace": 2426, "Oil refinery": 180, "Chemical plant": 299, "Assembling machine 3": 1622})
    )
)
def test_getNeededMachines(input, expected):
    assert main.getNeededMachines(input[0], input[1]) == expected

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