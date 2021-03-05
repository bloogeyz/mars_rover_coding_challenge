from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Dict, Any, List
import re

coords_pattern = r"\d+ \d+"
map_pattern = re.compile(f"^{coords_pattern}$")
rover_position_pattern = re.compile(f"^{coords_pattern} [NESW]$")
rover_movement_pattern = re.compile("^[LMR]+$")


@dataclass
class Direction(Enum):
    N = 0
    E = 90
    S = 180
    W = 270

    @staticmethod
    def from_int(value: int):
        if value == 0 or value == 360:
            return Direction.N
        elif value == 90:
            return Direction.E
        elif value == 180:
            return Direction.S
        elif value == 270 or value < 0:
            return Direction.W
        else:
            raise ValueError(f"Unexpected input: {value}")


@dataclass
class Instruction(Enum):
    L = -90
    R = 90
    M = 1


@dataclass
class Position:
    x: int
    y: int
    facing: Direction

    def __init__(self, x, y, facing: str):
        self.x = x
        self.y = y
        self.facing = Direction[facing]

    def rotate(self, instruction: Instruction):
        rotation = instruction.value
        new_direction = Direction.from_int(self.facing.value + rotation)
        self.facing = new_direction

    def move(self):
        if self.facing is Direction.N:
            self.y += 1
        elif self.facing is Direction.E:
            self.x += 1
        elif self.facing is Direction.S:
            self.y -= 1
        elif self.facing is Direction.W:
            self.x -= 1


@dataclass
class Plateau:
    max_x: Final[int]
    max_y: Final[int]
    grid: Dict[int, Dict[int, Any]] = field(default_factory=dict)

    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y
        # TODO: The grid attribute isn't used but I've set them up in case we ever wanted to check that rovers
        # aren't on top of each other
        inner_grid = {y: None for y in range(0, max_y)}
        self.grid = {x: inner_grid for x in range(0, max_x)}

    def valid_position(self, x: int, y: int) -> bool:
        return x <= self.max_x and y <= self.max_y


@dataclass
class Rover(Position):
    # TODO: Could use a UUID here for the id but it's overkill for the implementation
    id: int

    def __init__(self, rover_id: int, position_x: int, position_y: int, facing: str):
        super().__init__(x=position_x, y=position_y, facing=facing)
        self.id = rover_id

    def __str__(self):
        return f"{self.x} {self.y} {self.facing.name}"

    def read_instructions(self, mars_map: Plateau, instructions: str):
        for instruction in instructions:
            self.do_instruction(Instruction[instruction.upper()])
            if not mars_map.valid_position(self.x, self.y):
                raise ValueError(f"Rover {self.id} has gone off the map: x: {self.x} y: {self.y}")

    def do_instruction(self, instruction: Instruction):
        if instruction is Instruction.L or instruction is Instruction.R:
            self.rotate(instruction)
        else:
            assert instruction is Instruction.M
            self.move()


@dataclass
class InputResult:
    map: Plateau
    rovers: List[Rover]
    instructions: Dict[int, str]
