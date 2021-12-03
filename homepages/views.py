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

    lsSpecialty = ["Geriatric Psychiatry", "Hematology", "Podiatry", "Psychiatry & Neurology",
                    "Cardiology", "General Acute Care Hospital", "Pediatric Medicine", "Colorectal Surgery (formerly proctology)", "General Practice",
                    "Gastroenterology", "Multispecialty Clinic/Group Practice", "Interventional Pain Management", "CRNA", "Hospitalist",
                    "Plastic and Reconstructive Surgery", "Student in an Organized Health Care Education/Training Program", "Neurosurgery",
                    "Osteopathic Manipulative Medicine", "Physical Medicine and Rehabilitation", "Urology", "Pulmonary Disease",
                    "Pain Management", "Medical Oncology", "Unknown Physician Specialty Code", "Cardiac Electrophysiology",
                    "Geriatric Medicine", "Maxillofacial Surgery", "Allergy/Immunology", "Anesthesiology", "Hematology/Oncology",
                    "Otolaryngology", "Vascular Surgery", "Psychiatry", "Dermatology", "Community Health Worker",
                    "Gynecological/Oncology", "Rheumatology", "Nuclear Medicine", "Dentist", "Physician Assistant", "Sports Medicine", 
                    "Health Maintenance Organization", "Pharmacist", "Endocrinology", "Hospice and Palliative Care",
                    "Radiation Oncology", "Internal Medicine", "Infectious Disease", "Ophthalmology", "Legal Medicine", "Certified Nurse Midwife",
                    "Preventive Medicine", "Registered Nurse", "Orthopedic Surgery", "Surgical Oncology", "General Surgery", "Nurse", "Obstetrics/Gynecology", "Oral Surgery (dentists only)",
                    "Psychologist (billing independently)", "Optometry", "Critical Care (Intensivists)", "Neurology", "Specialist",
                    "Clinic/Center", "Thoracic Surgery", "Neuropsychiatry", "Nurse Practitioner", "Interventional Radiology", "Emergency Medicine", "Family Practice",
                    "Nephrology", "Diagnostic Radiology", "Cardiac Surgery", "Certified Clinical Nurse Specialist", "Family Medicine" ]


    context = {
        "prescriber" : data,
        "specialty" : lsSpecialty,
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
    Query1 = 'SELECT npi, drugname FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id  INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE pd_triple.qty > 0 AND npi = ' + str(prescriber_id)
    data2 = Prescriber.objects.raw(Query1)

    Query2 = 'SELECT 1 as id, pd_triple.drug_id, round(AVG(qty),0) AS avg FROM pd_triple GROUP BY drug_id HAVING drug_id IN (SELECT pd_triple.drug_id as id FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id  WHERE pd_triple.qty > 0 AND npi =' + str(prescriber_id) + ')'
    data3 = Triple.objects.raw(Query2)
    context = {
        "prescriber" : data,
        "drugsprescribed" : data2,
        "average" : data3
    }
    return render(request, 'homepages/prescriberDetails.html', context)


# View function to filter the prescriber
def filterPrescriberPageView(request) :

    # Collect the values from the filter form
    sFirst_Name = request.GET["first_name"]
    sLast_Name = request.GET["last_name"]
    sGender = request.GET["gender"]
    sCredentials = request.GET['credentials']
    sLocation = request.GET['location']

    # Transform to upper case
    sLocation = sLocation.upper()

    sSpeciality = request.GET['specialty']

    # Build the raw query
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
        sQuery += " AND specialty =" + "'" + sSpeciality + "'"

    # Run the raw query
    data = Prescriber.objects.raw(sQuery)

    # List with all the different specialty titles
    lsSpecialty = ["Geriatric Psychiatry", "Hematology", "Podiatry", "Psychiatry & Neurology",
                    "Cardiology", "General Acute Care Hospital", "Pediatric Medicine", "Colorectal Surgery (formerly proctology)", "General Practice",
                    "Gastroenterology", "Multispecialty Clinic/Group Practice", "Interventional Pain Management", "CRNA", "Hospitalist",
                    "Plastic and Reconstructive Surgery", "Student in an Organized Health Care Education/Training Program", "Neurosurgery",
                    "Osteopathic Manipulative Medicine", "Physical Medicine and Rehabilitation", "Urology", "Pulmonary Disease",
                    "Pain Management", "Medical Oncology", "Unknown Physician Specialty Code", "Cardiac Electrophysiology",
                    "Geriatric Medicine", "Maxillofacial Surgery", "Allergy/Immunology", "Anesthesiology", "Hematology/Oncology",
                    "Otolaryngology", "Vascular Surgery", "Psychiatry", "Dermatology", "Community Health Worker",
                    "Gynecological/Oncology", "Rheumatology", "Nuclear Medicine", "Dentist", "Physician Assistant", "Sports Medicine", 
                    "Health Maintenance Organization", "Pharmacist", "Endocrinology", "Hospice and Palliative Care",
                    "Radiation Oncology", "Internal Medicine", "Infectious Disease", "Ophthalmology", "Legal Medicine", "Certified Nurse Midwife",
                    "Preventive Medicine", "Registered Nurse", "Orthopedic Surgery", "Surgical Oncology", "General Surgery", "Nurse", "Obstetrics/Gynecology", "Oral Surgery (dentists only)",
                    "Psychologist (billing independently)", "Optometry", "Critical Care (Intensivists)", "Neurology", "Specialist",
                    "Clinic/Center", "Thoracic Surgery", "Neuropsychiatry", "Nurse Practitioner", "Interventional Radiology", "Emergency Medicine", "Family Practice",
                    "Nephrology", "Diagnostic Radiology", "Cardiac Surgery", "Certified Clinical Nurse Specialist", "Family Medicine" ]

    # Dictionary to pass the values to the HTML
    context = {
        "prescriber" : data,
        "specialty" : lsSpecialty,

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

    return render(request, 'homepages/addPrescriber.html')



    # View function to add a prescriber
def additionPrescriberPageView(request):
    if request.method == 'POST' :
        prescriber = Prescriber()
        prescriber.npi = request.POST['NPI']
        prescriber.fname = request.POST['first_name']
        prescriber.lname = request.POST['last_name']
        prescriber.gender = request.POST['gender']
        prescriber.state_id = request.POST['state']
        prescriber.credentials = request.POST['credentials']
        prescriber.specialty = request.POST['specialty']
        prescriber.totalprescriptions = request.POST['totalprescriptions']
        sOpioid = request.POST.get("sOpioid")

        if sOpioid in ["yes"]:
            sOpioid_Output = "TRUE"
        if sOpioid in ["no"]:
            sOpioid_Output = "FALSE"

        prescriber.isopioidprescriber = sOpioid_Output
        prescriber.save() 
    context = {

    }
    return addPageView(request)


# View function to display the edit prescriber html
def editPrescriberPageView(request, prescriber_id) : 
    data = Prescriber.objects.get(npi = prescriber_id)
    context = {
        "prescriber" : data,

    }

    return render(request, 'homepages/editPrescriber.html', context)

def updatePrescriberPageView(request) :
    if request.method == 'POST' :
        prescriber_id = request.POST['NPI']
        prescriber = Prescriber.objects.get(npi=prescriber_id)

        prescriber.npi = request.POST['NPI']
        prescriber.fname = request.POST['first_name']
        prescriber.lname = request.POST['last_name']
        prescriber.gender = request.POST['gender']
        prescriber.state_id = request.POST['state']
        prescriber.credentials = request.POST['credentials']
        prescriber.specialty = request.POST['specialty']
        prescriber.totalprescriptions = request.POST['totalprescriptions']
        sOpioid = request.POST.get("opioid")
        
        if sOpioid in ["yes"]:
            sOpioid_Output = "TRUE"
        if sOpioid in ["no"]:
            sOpioid_Output = "FALSE"

        prescriber.isopioidprescriber = sOpioid_Output
        
        prescriber.save()
     

    return savePageView(request)


# View function to display the edit prescriber save html
def savePageView(request) : 
    return render(request, 'homepages/save.html')

# View function to delete
def deletePageView(request, prescriber_id):
    data = Prescriber.objects.get(npi=prescriber_id)

    data.delete()

    return deletemessagePageView(request)

# View function to display the edit prescriber html
def deletemessagePageView(request) : 
    return render(request, 'homepages/delete.html')


# View function to display the edit prescriber html
def addPageView(request) : 
    return render(request, 'homepages/add.html')

# View function to display the prediction model
def predictionPageView(request) : 
    return render(request, 'homepages/predictionModel.html')

# View function to make a prediction
def makePredictionPageView(request) : 
    import requests
    import json

    # Grab the values from the prediction form
    drug_name = request.POST['drug_name']
    
    # Transform the variable to upper case
    drug_name = drug_name.upper()

    drug_object = Drug.objects.get(drugname=drug_name)
    drug_id = drug_object.drugid
    state = request.POST['state']
    # Transform the variable to upper case
    state = state.upper()
    population = request.POST['population']
    deaths = request.POST['deaths']
    totalprescriptions = request.POST['totalprescriptions']
    sOpioid = request.POST.get("sOpioid")
        
    # Determine whether they area opioid provider or not
    if sOpioid in ["yes"]:
        sOpioid_Output = "TRUE"
    if sOpioid in ["no"]:
        sOpioid_Output = "FALSE"


    # Set the sOpioid to the isopioidprescriber
    isopioidprescriber = sOpioid_Output
    
    url = "http://48387025-e221-44e6-9b7a-696b508b797f.eastus2.azurecontainer.io/score"

    payload = json.dumps({
        "Inputs": { 
            "WebServiceInput1": 
            [{"drugname": drug_name, 
            "stateabbrev": state, 
            "population": population, 
            "isopioidprescriber": isopioidprescriber,
            "deaths": deaths,
            "drugid": drug_id,
            "totalprescriptions": totalprescriptions
            }]
            },
            "GlobalParameters": {}
    })
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer FPY7svgpZAWBaDSROxBFlgHgVytRPnU3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    json_data = json.loads(response.text)

    for iCount in range(0, 1):
        sOutput = "Chances of prescriber prescribing an opioid: " + str(round(float((json_data['Results']['WebServiceOutput0'][iCount]['Scored Labels']) * 100), 2)) + "%"

    context = {
        "sOutput" : sOutput
    }
    return render(request, 'homepages/showPrediction.html', context)


