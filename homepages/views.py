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
    Query1 = 'SELECT npi, drugname FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id  INNER JOIN pd_drugs ON pd_triple.drugid = pd_drugs.drugid WHERE pd_triple.qty > 0 AND npi = ' + str(prescriber_id)
    data2 = Prescriber.objects.raw(Query1)

    # Query2 = 'SELECT drugid, round(AVG(qty),0) AS DrugAverage FROM pd_triple WHERE drugid = 2 GROUP BY drugid'
    # data3 = Triple.objects.raw(Query2)
    context = {
        "prescriber" : data,
        "drugsprescribed" : data2,
        # "average" : data3
        
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
    sQuery1 = "SELECT DISTINCT npi, specialty FROM pd_prescriber" # FIX THIS LATER
    specialty = Prescriber.objects.raw(sQuery1)
    context = {
        "prescriber" : data,
        "specialty" : specialty,

    }
    return render(request, 'homepages/showPrescribers.html', context)

# View function to filter the drugs
def filterDrugPageView(request) :
    sName = request.GET.get("drug_search")
    sName = sName.upper()
    bOpioid = request.GET.get("opioid")
   
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
    if request.method == 'POST' :
        prescriber = Prescriber()
        prescriber.npi = request.POST['NPI']
        prescriber.fname = request.POST['first_name']
        prescriber.lname = request.POST['last_name']
        prescriber.gender = request.POST['gender']
        prescriber.state_id = request.POST['state']
        prescriber.credentials = request.POST['credentials']
        prescriber.specialty = request.POST['specialty']

        sOpioid = request.GET.get("opioid")

        if sOpioid != '' :
            if sOpioid == 'yes' :
                sOpioid = True
            else :
                sOpioid = False

        prescriber.isopioidprescriber = sOpioid
        prescriber.save() 




    context = {

    }
    return render(request, 'homepages/addPrescriber.html', context)


# View function to display the edit prescriber html
def editPrescriberPageView(request, prescriber_id) : 
    data = Prescriber.objects.get(npi = prescriber_id)
    context = {
        "prescriber" : data,
    }

    return render(request, 'homepages/editPrescriber.html', context)

# def updatePrescriberPageView(request) :
#     if request.method == 'POST' :
#         cust_id = request.POST['cust_id']

#         customer = Customer.objects.get(id=cust_id)

#         customer.first_name = request.POST['first_name']
#         customer.last_name = request.POST['last_name']
#         customer.username = request.POST['username']
#         customer.password = request.POST['password']
#         customer.email = request.POST['email']
#         customer.phone = request.POST['phone']

#         customer.save()    

#     return render(request, 'homepages/showPrescribers.html')