from django.shortcuts import render

def home(request):
   return render(request, 'components/_setform.html')

def sets(request):
   operation = request.GET.get('sets')
   return render(request, 'sets.html', {'set_solved': operation})
