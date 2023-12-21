from django.shortcuts import render
from django.http import HttpResponse
from store.models import Collection

def say_hello(request):
    queryset = Collection.objects.filter(title="B")
   
    return render(request, 'hello.html', {'name':'Mosh','products':list(queryset)})
