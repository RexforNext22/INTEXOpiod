from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from .models import StateData
from .models import Prescriber, Drug, Triple

# Create your views here.

# Index page function/views
def indexPageView(request) :
    data = Drug.objects.all()
    context = {
        "drugs" : data,
    }
    return render(request, 'homepages/index.html', context)



def drugLibraryPageView(request) :


    return render(request, 'homepages/showDrugs.html')


def prescribersPageView(request) :
    return render(request, 'homepages/showPrescribers.html')
