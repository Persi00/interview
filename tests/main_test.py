import main
import pytest

@pytest.mark.parametrize(
    ("input", "expected"),
    (
        (("iron-plate", 1), {'Electric mining drill': 2, "Electric furnace": 2}),
        (("uranium-235", 1), {'Centrifuge': 1715, 'Electric mining drill': 5715}),
        (("uranium-238", 1), {'Centrifuge': 13, 'Electric mining drill': 41}),
        (("electronic-circuit", 1), {'Electric mining drill': 5, "Electric furnace": 5, "Assembling machine 3": 2}),
        (("speed-module", 1), {"Offshore pump": 1, "Electric mining drill": 105, "Pumpjack": 19, "Electric furnace": 76, "Oil refinery": 10, "Chemical plant": 5, "Assembling machine 3": 55}),
    )
)
def test_getNeededMachines(input, expected):
    print(input)
    assert main.getNeededMachines(input[0], input[1]) == expected