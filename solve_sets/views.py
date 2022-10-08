from django.shortcuts import render
from solve_sets.render_venn import graph_venn, is_renderable
from solve_sets.solve_sets import solve_sets


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
        {
            "set_solved": sets,
            "set_operations": operation,
            "set_venn": set_venn,
            "renderable": renderable,
        },
    )
