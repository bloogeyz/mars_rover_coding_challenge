# TODO: Hypothesis could also be used to create invalid scenarios in the other two tests
import pytest

from interpreter.interpret_string import read_input
from tests.conftest import invalid_inputs


@pytest.mark.parametrize("invalid_input, expected_response", invalid_inputs)
def test_read_input_returns_correct_error_with_invalid_input(invalid_input, expected_response):
    result = read_input(invalid_input)
    assert result.is_err()
    assert result.unwrap_err() == expected_response
