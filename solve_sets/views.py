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
    sets = item_to_lists(sets)
    operation = item_to_lists(operation)
    print(validate_operation(operation))


def format_sets(sets: str) -> str:
    return sets.replace(" ", "")


def item_to_lists(sets: str) -> list:
    return [str(set) for set in sets.split()]


def validate_sets(sets: list):
    valid_sets = []
    for set in sets:
        if matches := re.search(r"^([A-TV-Z])=\{(.+)+\}$", set):
            valid_sets.append(set)
    return valid_sets


def validate_operation(operations: list) -> list:
    valid_operations = []
    for operation in operations:
        if matches := re.search(r"^([A-TV-Z\-|&\(\)])+$", operation):
            valid_operations.append(operation)
    return valid_operations
