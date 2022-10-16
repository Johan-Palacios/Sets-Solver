# This file analizes sets in order to solve them properly with native functions

import re

# @param {sets}: string of sets
# @param {operation}: string of operations
# @returns valid operations and sets
def solve_sets(sets: str, operation: str):
    sets = format_sets(sets)
    operation = format_sets(operation)
    list_sets = item_to_lists(sets)
    list_operations = item_to_lists(operation)
    list_sets = validate_sets(list_sets)
    list_operations = validate_operation(list_operations)
    valid_operation, list_sets, universal_set = operate_set(list_sets, list_operations)
    return (list_sets, valid_operation, universal_set)


# @param {sets}: string of sets
# @returns string of sets without spaces
def format_sets(sets: str) -> str:
    return sets.replace(" ", "")


# @param {sets}: string of sets
# @param {param}: string to split data
# @returns a list of elements
def item_to_lists(sets: str, param=None) -> list:
    return [str(set) for set in sets.split(param)]


# @param {sets}: list of sets
# @returns a set() object
def validate_sets(sets: list):
    valid_sets = []
    for set_item in sets:
        if matches := re.search(r"^([A-TV-Z])=\{(.+)+\}$", set_item):
            try:
                valid_sets.append(
                    {
                        "setName": matches.group(1),
                        "setValue": set(item_to_lists(matches.group(2), ",")),
                    }
                )
            except:
                pass
    return valid_sets


# @param {operations}: list of operations
# @returns valid list of operations
def validate_operation(operations: list) -> list:
    valid_operations = []
    for operation in operations:
        if re.search(r"^([A-Z\-|\(\)&\^])+$", operation):
            valid_operations.append(operation)
    return valid_operations


# @param Sets list
# @return simple dict of sets
def simple_dict(sets: list):
    sets_data = {}
    universal_set = set()
    for item in sets:
        name = item.get("setName")
        value = item.get("setValue")
        if name in sets_data:
            continue
        sets_data[name] = value
        universal_set = universal_set | value
    sets_data["U"] = universal_set
    return sets_data, universal_set


# @param sets_data simple dict
# @return list with list of dictionaries
def complex_dict(sets_data: dict) -> list:
    list_sets = []
    for sets_name, sets_value in sets_data.items():
        if sets_name == "U":
            continue
        list_sets.append({"setName": str(sets_name), "setValue": sets_value})
    return list_sets


# @param {sets}: list of sets
# @param {operations}: list of operations
# @returns a list of operable sets and correct operations and universal set
def operate_set(sets: list, operations: list):
    solved_operation = []
    set_operation = []
    sets_data = {}
    sets_data, universal_set = simple_dict(sets)
    list_sets = complex_dict(sets_data)
    for operation in operations:
        set_operation = ""
        for variable in operation:
            set_operation += str(sets_data.get(variable, variable))
        try:
            safe_set_operation = eval(
                compile(set_operation, filename="", mode="eval"), {}, {}
            )
            solved_operation.append(
                {
                    "nameOperation": operation,
                    "operationValue": sorted(safe_set_operation),
                }
            )
        except:
            solved_operation.append(
                {
                    "nameOperation": operation,
                    "operationValue": "Error: Verifique su operación",
                }
            )
    return (solved_operation, list_sets, universal_set)


if __name__ == "__main__":
    pass
