from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# Import all the models
from .models import Drug
from .models import Triple
from .models import State
from .models import Prescriber

# Create your views here.

# Index page function/views
def indexPageView(request) :
    return render(request, 'homepages/index.html')


# View function to see all the drugs
def drugLibraryPageView(request) :
    data = Drug.objects.all()
    context = {
        "drugs" : data,
    }
    return render(request, 'homepages/showDrugs.html', context)

# View function to see all the prescribers
def prescribersPageView(request) :
    data = Prescriber.objects.all()
    sQuery1 = "SELECT DISTINCT npi, specialty FROM pd_prescriber" # FIX THIS LATER
    specialty = Prescriber.objects.raw(sQuery1)
    context = {
        "prescriber" : data,
        "specialty" : specialty,
    }
    return render(request, 'homepages/showPrescribers.html', context)

# View function to see the individual drug information
def drugDetailsPageView(request, drug_id):
    data = Drug.objects.get(drugid = drug_id)
    if data.isopioid == True :
        opioid = "Opioid"
    else:
        opioid = "Not Opioid"

    data2 = data.drugname.all()
    data3 = Triple.objects.get(drugname = data2)
    data4 = data3.prescriber_id.all()
    data5 = Prescriber.objects.get(npi = data4)
    context = {
        "drug" : data,
        "opioid" : opioid,
        "topprescriber" : data5
    }
    return render(request, 'homepages/drugDetails.html', context)

# View function to view the individual prescribers
def viewPrescriberPageView(request, prescriber_id) :
    data = Prescriber.objects.get(npi = prescriber_id)
    Query1 = 'SELECT drugname FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id'
    # listdrugs = Prescriber.npi.drugname.all()
    context = {
        "prescriber" : data,
        # "listdrugs" : listdrugs
    }
    return render(request, 'homepages/prescriberDetails.html', context)


# View function to filter the prescriber
def filterPrescriberPageView(request) :
    sFirst_Name = request.GET["first_name"]
    sLast_Name = request.GET["last_name"]
    sGender = request.GET["gender"]
    sCredentials = request.GET['credentials']
    sLocation = request.GET['location']
    sSpeciality = request.GET['specialty']
    sQuery = "SELECT * FROM pd_prescriber WHERE pd_prescriber.npi = pd_prescriber.npi"
    if sFirst_Name != '' :
        sQuery += " AND fname = " + "'" + sFirst_Name + "'"

    if sLast_Name != '' :
        sQuery += " AND lname = " + "'" + sLast_Name + "'"
    
    if sGender != '' :
        sQuery += " AND gender = " + "'" + sGender + "'"

    if sLocation != '' :
        sQuery += " AND state_id = " + "'" + sLocation + "'"

    if sCredentials != '' :
        sQuery += " AND credentials = " + "'" + sCredentials + "'"

    if sSpeciality != '' :
        sQuery += " AND specialty LIKE " + "'%" + sSpeciality + "%'"
    data = Prescriber.objects.raw(sQuery)
    context = {
        "prescriber" : data,

    }
    return render(request, 'homepages/showPrescribers.html', context)

# View function to add a prescriber
def addPrescriberPageView(request):





    context = {

    }
    return render(request, 'homepages/addPrescriber.html', context)