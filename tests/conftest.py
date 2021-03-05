invalid_inputs = [
    (
        """5 5""",
        "Input in incorrect format, expected at least 3 lines got 1",
    ),
    (
        """5 5
        1 2 N""",
        "Invalid input: expected an odd number of lines, got 2",
    ),
    (
        """5 5
        1 2 N
        L
        1 2 E""",
        "Invalid input: expected an odd number of lines, got 4",
    ),
    (
        """A B
        1 2 N
        L""",
        "Map did not match expected format.",
    ),
    (
        """1
        1 2 N
        L""",
        "Map did not match expected format.",
    ),
    (
        """1 2 3
        1 2 N
        L""",
        "Map did not match expected format.",
    ),
    (
        """5 5
        1 2 A
        LML""",
        "Positional data for rover 1 is not in the correct format: 1 2 A",
    ),
    (
        """5 5
        1 2
        LML""",
        "Positional data for rover 1 is not in the correct format: 1 2",
    ),
    (
        """5 5
        1 2 S W
        LML""",
        "Positional data for rover 1 is not in the correct format: 1 2 S W",
    ),
]

invalid_rover_paths = [
    (
        """5 5
    1 2 N
    LMM""",
        "Rover 0 has gone off the map: x: -1, y: 2",
    ),
    (
        """7 2
    1 1 E
    RM
    5 0 W
    RRMMM""",
        "Rover 1 has gone off the map: x: 8, y: 0",
    ),
    (
        """1 2
    1 1 N
    MRRMMM""",
        "Rover 0 has gone off the map: x: 1, y: -1",
    ),
    (
        """10 10
    1 6 E
    LMMMMM""",
        "Rover 0 has gone off the map: x: 1, y: 11",
    ),
]
