from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from .models import Drug
from .models import Triple
from .models import State
from .models import Prescriber

# Create your views here.

# Index page function/views
def indexPageView(request) :
    return render(request, 'homepages/index.html')



def drugLibraryPageView(request) :
    data = Drug.objects.all()
    context = {
        "drugs" : data,
    }
    return render(request, 'homepages/showDrugs.html', context)


def prescribersPageView(request) :
    data = Prescriber.objects.all()
    context = {
        "prescriber" : data,
    }
    return render(request, 'homepages/showPrescribers.html', context)

def viewPrescriberPageView(request, presriber_id) :
    data = Prescriber.objects.all()
    context = {
        "prescriber" : data,
    }
    return render(request, 'homepages/prescriberDetails.html', context)
