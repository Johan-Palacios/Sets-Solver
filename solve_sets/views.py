from django.shortcuts import render
import re


def home(request):
    return render(request, "components/_setform.html")


def sets(request):
    sets = request.GET.get("sets")
    operation = request.GET.get("sets_operation")
    solve_sets(str(sets), str(operation))
    return render(request, "sets.html", {"set_solved": sets})


def solve_sets(sets: str, operation: str):
    sets = format_sets(sets)
    operation = format_sets(operation)
    list_sets = item_to_lists(sets)
    list_operations = item_to_lists(operation)
    list_sets = validate_sets(list_sets)
    list_operations = validate_operation(list_operations)
    valid_sets, valid_operation = operate_set(list_sets, list_operations)
    print(valid_sets, valid_operation)


def format_sets(sets: str) -> str:
    return sets.replace(" ", "")


def item_to_lists(sets: str, param=None) -> list:
    return [str(set) for set in sets.split(param)]


def append_set(elements: list) -> set:
    return set(str(element) for element in elements)


def validate_sets(sets: list):
    valid_sets = []
    for set in sets:
        if matches := re.search(r"^([A-TV-Z])=\{(.+)+\}$", set):
            try:
                valid_sets.append(
                    {
                        "setName": matches.group(1),
                        "setValue": append_set(item_to_lists(matches.group(2), ",")),
                    }
                )
            except:
                pass
    return valid_sets


def validate_operation(operations: list) -> list:
    valid_operations = []
    for operation in operations:
        if re.search(r"^([A-TV-Z\-|&\(\)])+$", operation):
            valid_operations.append(operation)
    return valid_operations


def operate_set(sets: list, operations: list):
    operable_sets = []
    correct_operations = []
    for set in sets:
        set_name = str(set["setName"])
        set_value = set["setValue"]
        try:
            exec(f"{set_name} = set_value")
            operable_sets.append({"set": set_name, "setValue": set_value })
        except:
            pass
    for operation in operations:
        try:
            correct_operations.append(
                {"operation": operation, "result": sorted(eval(operation))}
            )
        except:
            correct_operations.append(
                {
                    "operation": operation,
                    "result": "Error al operar, verifique su operación",
                }
            )
    return operable_sets, correct_operations
