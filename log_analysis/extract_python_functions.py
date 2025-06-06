#!/usr/bin/env python

import argparse
import ast
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract Python functions from a file and write them to separate files."
    )
    parser.add_argument(
        "file_paths",
        type=str,
        help="Path to the Python file to extract functions from.",
        nargs="+",
    )
    return parser.parse_args()


def extract_functions_from_file(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    return functions


def write_function_to_file(function, original_file_name):
    function_name = function.name
    file_name = f"{function_name}_{original_file_name}.txt"
    with open(file_name, "w") as file:
        file.write(ast.unparse(function))


def extract_and_write_functions(file_path):
    original_file_name = os.path.basename(file_path).replace(".py", "")
    functions = extract_functions_from_file(file_path)
    for function in functions:
        write_function_to_file(function, original_file_name)


if __name__ == "__main__":
    args = parse_arguments()
    for file_path in args.file_paths:
        extract_and_write_functions(file_path)
