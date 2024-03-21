from django.shortcuts import render
from django.http import HttpResponse

 

def signUp(request):
    return HttpResponse("this is signup page")

def home(request):
    data={
        'title':'html page',
        'h':'thats the new page',
        'list':['first','second','third']
    }
 
    return render(request,'home.html',data)

