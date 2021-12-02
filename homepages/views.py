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
  
    query1 = 'SELECT npi, fname, lname, qty FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id INNER JOIN pd_drugs ON pd_triple.drugid = pd_drugs.drugid WHERE pd_drugs.drugid =' + str(drug_id) + ' ORDER BY pd_triple.qty DESC LIMIT 10'
    data2 = Prescriber.objects.raw(query1)
    context = {
        "drug" : data,
        "opioid" : opioid,
        "topprescriber" : data2
    }
    return render(request, 'homepages/drugDetails.html', context)


# View function to view the individual prescribers
def viewPrescriberPageView(request, prescriber_id) :
    data = Prescriber.objects.get(npi = prescriber_id)

    # Pull the prescribers for this drug
    Query1 = 'SELECT npi, drugname, drugid FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id  INNER JOIN pd_drugs ON pd_triple.drugid = pd_drugs.drugid WHERE pd_triple.qty > 0 AND npi = ' + str(prescriber_id)
    data2 = Prescriber.objects.raw(Query1)

    Query2 = 'SELECT drugid, round(AVG(qty),0) AS DrugAverage FROM pd_triple WHERE drugid =' + data2.drugid + 'GROUP BY drugid'
    data3 = Triple.objects.raw(Query2)
    context = {
        "prescriber" : data,
        "drugsprescribed" : data2,
        "average" : data3
        
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

# View function to filter the drugs
def filterDrugPageView(request) :
    sName = request.GET["drug_name"]
    bOpioid = request.GET["Opioid"]
   
    sQuery = "SELECT * FROM pd_drugs WHERE pd_drugs.drugid = pd_drugs.drugid"
    if sName != '' :
        sQuery += " AND drugname = " + "'" + sName + "'"

    if bOpioid != '' :
        if bOpioid == 'yes' :
            bOpioid = 'True'
        else :
            bOpioid = 'False'
        
        sQuery += " AND isopioid = " + "'" + bOpioid + "'"
 
    data = Drug.objects.raw(sQuery)
    context = {
        "drugs" : data,

    }
    return render(request, 'homepages/showDrugs.html', context)



# View function to add a prescriber
def addPrescriberPageView(request):





    context = {

    }
    return render(request, 'homepages/addPrescriber.html', context)