from typing import List, Any

from result import Result, Err, Ok

from interpreter import handle_input


def process_rover_routes(rover_input: Any) -> Result[List[str], str]:
    # TODO: Expand this to take other formats, namely from a text file and dictionary input
    input_result = handle_input(rover_input)
    if input_result.is_err():
        return Err(input_result.unwrap_err())
    mars_rover_data = input_result.unwrap()

    final_positions: List[str] = []
    for rover in mars_rover_data.rovers:
        try:
            rover.read_instructions(mars_rover_data.map, mars_rover_data.instructions[rover.id])
        except ValueError as e:
            return Err(str(e))
        final_positions.append(str(rover))
    return Ok(final_positions)
