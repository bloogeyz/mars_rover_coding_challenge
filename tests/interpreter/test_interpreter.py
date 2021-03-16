import pathlib

import pytest

from interpreter import handle_input


@pytest.mark.parametrize(
    ("valid_input", "expected_type"),
    [(["random", "list"], "list"), (open(pathlib.Path(__file__).parent / "test_data/rover_input.csv"), "csv")],
)
def test_handle_input_with_invalid_types(valid_input, expected_type):
    input_response = handle_input(valid_input)
    assert input_response.is_err()
    assert input_response.err() == f"Unexpected input format: {expected_type}"
