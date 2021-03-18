from result import Err

from interpreter.interpret_string import read_input as read_input_string
from interpreter.interpret_txt import read_input as read_input_txt
from interpreter.interpret_xml import read_input as read_input_xml
from interpreter.interpret_dict import read_input as read_input_dict

interpret_factory = {"str": read_input_string, "dict": read_input_dict, "txt": read_input_txt, "xml": read_input_xml}


def handle_input(input):
    file_type = type(input).__name__
    if file_type == "TextIOWrapper":
        file_type = input.name.rsplit(".", 1)[1]
    if file_type not in interpret_factory:
        return Err(f"Unexpected input format: {file_type}")
    return interpret_factory[file_type](input)
