import pytest

from hypothesis import given

from rover_logic import process_rover_routes
from tests.conftest import invalid_rover_paths
from tests.strategies import random_input_generation


def test_complete_route_standard_input():
    rover_input = """5 5
    1 2 N
    LMLMLMLMM
    3 3 E
    MMRMMRMRRM"""
    expected_output = ["1 3 N", "5 1 E"]
    completed_route_result = process_rover_routes(rover_input)
    assert completed_route_result.is_ok()
    assert completed_route_result.unwrap() == expected_output


@given(random_input_generation())
def test_complete_route_hypothesis(random_input):
    """This test relies on the hypothesis library to test a variety of random interpreter within bounds"""
    completed_route_result = process_rover_routes(random_input)
    assert completed_route_result.is_ok()


@pytest.mark.parametrize("invalid_rover_path, expected_response", invalid_rover_paths)
def test_correct_response_when_rover_goes_off_map(invalid_rover_path, expected_response):
    completed_route_result = process_rover_routes(invalid_rover_path)
    assert completed_route_result.is_err()
    assert completed_route_result.unwrap_err() == expected_response
