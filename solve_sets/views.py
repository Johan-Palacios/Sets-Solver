from django.shortcuts import render

def home(request):
   return render(request, 'home.html')

def sets(request):
   operation = request.GET.get('sets')
   return render(request, 'sets.html', {'set_solved': operation})
