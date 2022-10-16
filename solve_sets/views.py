from django.shortcuts import render
from solve_sets.solve_sets import solve_sets
from solve_sets.render_venn import graph_venn, is_renderable


def home(request):
    return render(request, "components/_setform.html")


def usage(request):
    return render(request, "usage.html")


def sets(request):
    sets = request.GET.get("sets")
    operation = request.GET.get("sets_operation")
    sets, operation, universal_set = solve_sets(str(sets), str(operation))
    set_venn = graph_venn(sets)
    renderable = is_renderable(len(sets))
    return render(
        request,
        "sets.html",
        {
            "set_solved": sets,
            "set_operations": operation,
            "universal": universal_set,
            "set_venn": set_venn,
            "renderable": renderable,
        },
    )
