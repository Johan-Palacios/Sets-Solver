from django.shortcuts import render
import re
import io
import urllib.parse, base64
from matplotlib import pyplot as plt
from matplotlib_venn import venn2
import os
# from sympy import FiniteSet


def home(request):
    return render(request, "components/_setform.html")


def sets(request):
    sets = request.GET.get("sets")
    operation = request.GET.get("sets_operation")
    sets, operation =solve_sets(str(sets), str(operation))
    A = sets[0]["setValue"]
    B = sets[1]["setValue"]
    A_label = sets[0]["setName"]
    B_label = sets[1]["setName"]
    v = None
    set_venn = None
    v = graph_venn2(A,B,A_label, B_label)
    set_venn = render_venn(v)
    return render(request, "sets.html", {"set_solved": sets + operation, "set_venn": set_venn})


def render_venn(v):
    plt.get(v)
    data = io.BytesIO()
    plt.savefig(data, format='png')
    b64 = base64.b64encode(data.getvalue()).decode()
    data.flush()
    data.seek(0)
    plt.close()
    return b64

def graph_venn2(A:set, B:set, A_label: str, B_label: str):
    v = venn2((A,B),(A_label, B_label), alpha=0.4)
    labels = [[A-B], [A&B], [B-A]]
    if labels[1] == [set()]:
        v.get_label_by_id('01').set_text(str(sorted(labels[2])))
        v.get_label_by_id('10').set_text(str(sorted(labels[0])))
    elif labels[2] == [set()]:
        v.get_label_by_id('11').set_text(str(sorted(labels[1])))
        v.get_label_by_id('10').set_text(str(sorted(labels[0])))
        v.get_label_by_id('01').set_text(str(""))
    elif labels[0] == [set()]:
        v.get_label_by_id('01').set_text(str(sorted(labels[2])))
        v.get_label_by_id('11').set_text(str(sorted(labels[1])))
        v.get_label_by_id('10').set_text(str(""))
    else:
        v.get_label_by_id('10').set_text(str(sorted(labels[0])))
        v.get_label_by_id('11').set_text(str(sorted(labels[1])))
        v.get_label_by_id('01').set_text(str(sorted(labels[2])))
    return v

def solve_sets(sets: str, operation: str):
    sets = format_sets(sets)
    operation = format_sets(operation)
    list_sets = item_to_lists(sets)
    list_operations = item_to_lists(operation)
    list_sets = validate_sets(list_sets)
    list_operations = validate_operation(list_operations)
    valid_sets, valid_operation = operate_set(list_sets, list_operations)
    return (valid_sets, valid_operation)


def format_sets(sets: str) -> str:
    return sets.replace(" ", "")


def item_to_lists(sets: str, param=None) -> list:
    return [str(set) for set in sets.split(param)]

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


def validate_operation(operations: list) -> list:
    valid_operations = []
    for operation in operations:
        if re.search(r"^([A-TV-Z\-|\(\)&])+$", operation):
            valid_operations.append(operation)
    return valid_operations


def operate_set(sets: list, operations: list):
    operable_sets = []
    correct_operations = []
    for set_item in sets:
        set_name = str(set_item["setName"])
        set_value = set_item["setValue"]
        try:
            exec(f"{set_name} = set_value")
            operable_sets.append({"setName": set_name, "setValue": set_value })
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
