#!/usr/bin/env python

import subprocess
import sys
import pathlib


def is_path_module(path) -> bool:
    path = pathlib.Path(path)
    parts = path.parts
    if "plugins" in parts and "modules" in parts:
        # print(f"This is module {str(parts[-1])}")
        return True
    return False


def is_path_integration_test(path) -> bool:
    path = pathlib.Path(path)
    parts = path.parts
    if "integration" in parts and "tests" in parts:
        return True
    return False


def get_module_name_from_module(path) -> str:
    path = pathlib.Path(path)
    parts = path.parts
    return parts[-1].split(".")[0]


def get_module_name_from_test(path) -> str:
    path = pathlib.Path(path)
    parts = path.parts
    return parts[-3]


def execute_tests(module_name) -> None:
    subprocess.run(
        ["ansible-test", "network-integration", "--allow-unsupported", module_name]
    )


def main():
    if len(sys.argv) == 1:
        sys.exit("File path must be passed as an argument.")
    if is_path_module(sys.argv[1]) is True:
        module_name = get_module_name_from_module(sys.argv[1])
    if is_path_integration_test(sys.argv[1]) is True:
        module_name = get_module_name_from_test(sys.argv[1])
    exit(module_name)
    # execute_tests(module_name)


if __name__ == "__main__":
    main()
