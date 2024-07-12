import main
import pytest

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        (("iron-plate", 1), {'Electric mining drill': 2, "Electric furnace": 2}),
        (("uranium-235", 1), {'Centrifuge': 1716, 'Electric mining drill': 5720}),
        (("uranium-238", 1), {'Centrifuge': 24, 'Electric mining drill': 80}),
        (("electronic-circuit", 1), {'Electric mining drill': 6, "Electric furnace": 6, "Assembling machine 3": 2}),
        # (("speed-module", 1), {'iron-ore': 15, 'copper-ore': 33, 'coal': 5, 'water': 100, 'crude-oil': 200}),
        # (("explosive-uranium-cannon-shell", 1), {'iron-ore': 10, 'coal': 2, 'crude-oil': 100, 'water': 90, 'uranium-ore': 20}),
    )
)
def test_getNeededMachines(input, expected):
    print(input)
    assert main.getNeededMachines(input[0], input[1]) == expected