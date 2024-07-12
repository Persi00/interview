import main
import pytest

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        (("iron-plate", 1), {'iron-ore': 1}),
        (("uranium-235", 1), {'uranium-ore': 1430}),
        (("uranium-238", 1), {'uranium-ore': 20}),
        (("electronic-circuit", 1), {'copper-ore': 2, 'iron-ore': 1}),
        (("speed-module", 1), {'iron-ore': 15, 'copper-ore': 33, 'coal': 5, 'water': 100, 'crude-oil': 200}),
        (("explosive-uranium-cannon-shell", 1), {'iron-ore': 10, 'coal': 2, 'crude-oil': 100, 'water': 90, 'uranium-ore': 20})
    )
)
def test_getNeededResourcesAndMachines(input, expected):
    assert main.getNeededResourcesAndMachines(input[0], input[1]) == expected