import re
from typing import List

from result import Result, Err, Ok
from data_types import map_pattern, Plateau, rover_position_pattern, rover_movement_pattern, Rover, InputResult


def build_map(map_string: str) -> Result[Plateau, str]:
    if not re.match(map_pattern, map_string):
        return Err("Map did not match expected format.")
    split_coordinates = map_string.split()
    return Ok(Plateau(int(split_coordinates[0]), int(split_coordinates[1])))


def build_rover(rover_position_as_string: str, rover_id: int) -> Result[Rover, str]:
    if not re.match(rover_position_pattern, rover_position_as_string):
        return Err(f"Positional data for rover {rover_id + 1} is not in the correct format: {rover_position_as_string}")

    split_position = rover_position_as_string.split()
    try:
        position_x = int(split_position[0])
        position_y = int(split_position[1])
        direction = split_position[2].upper()
    except TypeError as e:
        return Err(str(e))
    return Ok(Rover(rover_id=rover_id, position_x=position_x, position_y=position_y, facing=direction))


def read_input(input: str) -> Result[InputResult, str]:
    rover_list = []
    instructions = {}
    split_input = input.splitlines()
    assert len(split_input) > 2, f"Input in incorrect format, expected at least 3 lines got {len(split_input)}"
    assert len(split_input) % 2 != 0, f"Invalid input: {input}, an odd number of lines in expected"
    map_result = build_map(split_input[0].strip())
    if map_result.is_err():
        return Err(map_result.unwrap_err())
    for count, input_line in enumerate(range(1, len(split_input), 2)):
        rover_result = build_rover(split_input[input_line].strip(), count)
        if rover_result.is_err():
            return Err(rover_result.unwrap_err())
        rover_list.append(rover_result.unwrap())

        rover_movement_as_string = split_input[input_line + 1].strip()
        if not re.match(rover_movement_pattern, rover_movement_as_string):
            return Err(f"Movement data for rover {count + 1} is not in the correct format: {rover_movement_as_string}")
        instructions[count] = rover_movement_as_string

    return Ok(InputResult(map_result.unwrap(), rover_list, instructions))


def complete_route(input) -> Result[List[str], str]:
    input_result = read_input(input)
    if input_result.is_err():
        return Err(input_result.unwrap_err())
    mars_rover_data = input_result.unwrap()

    final_positions = []
    for rover in mars_rover_data.rovers:
        rover.read_instructions(mars_rover_data.map, mars_rover_data.instructions[rover.id])
        final_positions.append(str(rover))
    return Ok(final_positions)
