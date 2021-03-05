from rover_logic import complete_route


def test_rover_logic():
    rover_input = """5 5
    1 2 N
    LMLMLMLMM
    3 3 E
    MMRMMRMRRM"""
    expected_output = ["1 3 N", "5 1 E"]
    completed_route_result = complete_route(rover_input)
    assert completed_route_result.is_ok()
    assert completed_route_result.unwrap() == expected_output
