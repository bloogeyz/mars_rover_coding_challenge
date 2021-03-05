from typing import Tuple

import hypothesis.strategies as st
from hypothesis import assume
from hypothesis.strategies import composite


random_direction = st.sampled_from("NSWE")
random_instruction = st.sampled_from("LRM")

clockwise_pos_map = {"N": "E", "E": "S", "S": "W", "W": "N"}
anticlockwise_pos_map = {v: k for k, v in clockwise_pos_map.items()}


def apply_instruction(current_pos, next_instruction) -> Tuple[int, int, str]:
    if next_instruction == "L":
        return current_pos[0], current_pos[1], anticlockwise_pos_map[current_pos[2]]
    elif next_instruction == "R":
        return current_pos[0], current_pos[1], clockwise_pos_map[current_pos[2]]
    elif next_instruction == "M":
        if current_pos[2] == "N":
            return current_pos[0], current_pos[1] + 1, current_pos[2]
        elif current_pos[2] == "E":
            return current_pos[0] + 1, current_pos[1], current_pos[2]
        elif current_pos[2] == "S":
            return current_pos[0], current_pos[1] - 1, current_pos[2]
        elif current_pos[2] == "W":
            return current_pos[0] - 1, current_pos[1], current_pos[2]
        else:
            raise ValueError(f"{current_pos[2]} is not a valid direction")
    else:
        raise ValueError(f"Hypothesis gave invalid input: {next_instruction}")


@composite
def random_input_generation(draw):
    map_size_x = draw(st.integers(min_value=1, max_value=100000))
    map_size_y = draw(st.integers(min_value=1, max_value=100000))
    rover_input_string = f"{map_size_x} {map_size_y}\n"
    for i in range(0, draw(st.integers(min_value=1, max_value=50))):
        rover_x = draw(st.integers(min_value=0, max_value=map_size_x))
        rover_y = draw(st.integers(min_value=0, max_value=map_size_y))
        rover_direction = draw(random_direction)
        instructions = ""
        current_pos = (rover_x, rover_y, rover_direction)
        for j in range(0, draw(st.integers(min_value=1, max_value=50))):
            next_instruction = draw(random_instruction)
            current_pos = apply_instruction(current_pos, next_instruction)
            assume(0 <= current_pos[0] < map_size_x)
            assume(0 <= current_pos[1] < map_size_y)
            instructions += next_instruction
        rover_string = f"""{rover_x} {rover_y} {rover_direction}
                        {instructions}\n"""
        rover_input_string += rover_string
    return rover_input_string
