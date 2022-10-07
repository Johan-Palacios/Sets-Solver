import re
import ast
import io
import base64
from django.shortcuts import render
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3


def home(request):
    return render(request, "components/_setform.html")

def usage(request):
    return render(request, "usage.html")

def sets(request):
    sets = request.GET.get("sets")
    operation = request.GET.get("sets_operation")
    sets, operation = solve_sets(str(sets), str(operation))
    set_venn = graph_venn(sets)
    renderable = is_renderable(len(sets))
    return render(
        request,
        "sets.html",
        {"set_solved": sets, "set_operations": operation, "set_venn": set_venn, "renderable":renderable},
    )


# @param {sets_number}: number of sets
# @returns Bool
def is_renderable(sets_number: int):
    return sets_number == 2 or sets_number == 3


# @param {v}: Venn Diagram
# @returns: String base64, format png of Venn Diagram
def render_venn(v):
    plt.get(v)
    data = io.BytesIO()
    plt.savefig(data, format="png")
    b64 = base64.b64encode(data.getvalue()).decode()
    data.flush()
    data.seek(0)
    plt.clf()
    plt.close()
    return b64


# @param {A}: set
# @param {B}: set
# @param {a_label}: Set A name
# @param {b_label}: Set B name
# @returns: matiplot Venn diagram
def graph_venn2(A: set, B: set, a_label: str, b_label: str):
    v = venn2(([A, B]), (a_label, b_label), alpha=0.4)
    venn_data = [
        {"id": "10", "text_value": "\n".join(sorted(A - B))},
        {"id": "01", "text_value": "\n".join(sorted(B - A))},
        {"id": "11", "text_value": "\n".join(sorted(A & B))},
    ]
    v = set_text_venn(venn_data, v)
    plt.title(f"Diagrama entre {a_label} y {b_label}")
    return v


# @param {A}: set
# @param {B}: set
# @param {C}: set
# @param {a_label}: Set A name
# @param {b_label}: Set B name
# @param {c_label}: Set C Name
# @returns: matiplot Venn diagram
def graph_venn3(A: set, B: set, C: set, a_label: str, b_label: str, c_label: str):
    v = venn3(((A, B, C)), (a_label, b_label, c_label), alpha=0.4)
    venn_data = [
        {"id": "100", "text_value": "\n".join(sorted(A - B - C))},
        {"id": "110", "text_value": "\n".join(sorted(A & B - C))},
        {"id": "010", "text_value": "\n".join(sorted(B - C - A))},
        {"id": "101", "text_value": "\n".join(sorted(A & C - B))},
        {"id": "111", "text_value": "\n".join(sorted(A & B & C))},
        {"id": "011", "text_value": "\n".join(sorted(B & C - A))},
        {"id": "001", "text_value": "\n".join(sorted(C - B - A))},
    ]
    v = set_text_venn(venn_data, v)
    plt.title(f"Diagrama de venn entre {a_label}, {b_label} y {c_label}")
    return v


# @param { data }: list of ID
# @param { v }: matiplot venn graph
def set_text_venn(data: list, v):
    for item in data:
        try:
            v.get_label_by_id(item["id"]).set_text(item["text_value"])
        except:
            pass
    return v


# @param {sets}: group of sets
# @returns a Graphical Venn
def graph_venn(sets):
    if is_renderable(len(sets)):
        if len(sets) == 2:
            v = graph_venn2(
                sets[0]["setValue"],
                sets[1]["setValue"],
                sets[0]["setName"],
                sets[1]["setName"],
            )
            return render_venn(v)
        else:
            v = graph_venn3(
                sets[0]["setValue"],
                sets[1]["setValue"],
                sets[2]["setValue"],
                sets[0]["setName"],
                sets[1]["setName"],
                sets[2]["setName"],
            )
            return render_venn(v)


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
    valid_sets, valid_operation = operate_set(list_sets, list_operations)
    return (valid_sets, valid_operation)


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
        if re.search(r"^([A-TV-Z\-|\(\)&])+$", operation):
            valid_operations.append(operation)
    return valid_operations


# @param {sets}: list of sets
# @param {operations}: list of operations
# @returns a list of operable sets and correct operations
def operate_set(sets: list, operations: list):
    operable_sets = []
    correct_operations = []
    set_value = None
    for set_item in sets:
        set_name = str(set_item["setName"])
        set_value = set_item["setValue"]
        try:
            set_init = ast.parse(f"{set_name} = set_value")
            exec(compile(set_init, filename="", mode="exec"))
            operable_sets.append({"setName": set_name, "setValue": set_value})
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
