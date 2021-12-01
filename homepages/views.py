from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.

# Index page function/views
def indexPageView(request) :
    return render(request, 'homepages/index.html')
