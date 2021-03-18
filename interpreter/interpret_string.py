import re
from typing import List, Dict, Tuple

from result import Err, Ok, Result

from data_types import rover_movement_pattern, InputResult, Rover, rover_position_pattern, Plateau, map_pattern


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


def build_rovers_and_instructions(rover_and_instruction_pairs: List[str]) -> Result[
    tuple[list[Rover], dict[int, str]], str]:
    rover_list: List[Rover] = []
    instructions: Dict[int, str] = {}
    for count, input_line in enumerate(range(0, len(rover_and_instruction_pairs), 2)):
        rover_result = build_rover(rover_and_instruction_pairs[input_line].strip(), count)
        if rover_result.is_err():
            return Err(rover_result.unwrap_err())
        rover_list.append(rover_result.unwrap())

        rover_movement_as_string = rover_and_instruction_pairs[input_line + 1].strip()
        if not re.match(rover_movement_pattern, rover_movement_as_string):
            return Err(f"Movement data for rover {count + 1} is not in the correct format: {rover_movement_as_string}")
        instructions[count] = rover_movement_as_string
    return Ok((rover_list, instructions))


def read_input(rover_input: str) -> Result[InputResult, str]:
    split_input = rover_input.strip().splitlines()
    if len(split_input) < 2:
        return Err(f"Input in incorrect format, expected at least 3 lines got {len(split_input)}")
    if len(split_input) % 2 == 0:
        return Err(f"Invalid input: expected an odd number of lines, got {len(split_input)}")

    map_result = build_map(split_input[0].strip())
    if map_result.is_err():
        return Err(map_result.unwrap_err())

    rover_result = build_rovers_and_instructions(split_input[1:])
    if rover_result.is_err():
        return Err(rover_result.unwrap_err())
    rover_list, instructions = rover_result.unwrap()

    return Ok(InputResult(map_result.unwrap(), rover_list, instructions))
