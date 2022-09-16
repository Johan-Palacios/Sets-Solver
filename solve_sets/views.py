from django.shortcuts import render

def home(request):
   return render(request, 'components/_setform.html')

def sets(request):
   sets = request.GET.get('sets')
   solve_sets(str(sets))
   return render(request, 'sets.html', {'set_solved': sets})

def solve_sets(sets:str):
   pass

def format_sets():
   return sets.replace(" ", "")
