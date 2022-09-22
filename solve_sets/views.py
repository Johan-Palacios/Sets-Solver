from django.shortcuts import render

def home(request):
    return render(request, 'components/_setform.html')


def sets(request):
    sets = request.GET.get('sets')
    solve_sets(str(sets))
    return render(request, 'sets.html', {'set_solved': sets})

def solve_sets(sets: str):
    sets = format_sets(sets)
    print(sets_to_lists(sets))

def format_sets(sets: str) -> str:
    return sets.replace(" ", "")

def sets_to_lists(sets: str) -> list:
    return [str(set) for set in sets.split()]
