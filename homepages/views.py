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

# Index 2 function
def index2PageView(request) :
    return render(request, 'homepages/index2.html')


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

    # Dictionary with the specialities
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
  
    query1 = 'SELECT npi, fname, lname, qty FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE pd_drugs.drugid =' + str(drug_id) + ' ORDER BY pd_triple.qty DESC LIMIT 10'
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

    # Create the output message to the screen
    for iCount in range(0, 1):
        sOutput = "Chances of presciption for an opioid: " + str(round(float((json_data['Results']['WebServiceOutput0'][iCount]['Scored Labels']) * 100), 2)) + "%"

    # Dictionary to pass to the prediction page
    context = {
        "sOutput" : sOutput
    }
    return render(request, 'homepages/showPrediction.html', context)

# View function to display the recommender model
def showRecommenderPageView(request) : 
    return render(request, 'homepages/showRecommender.html')

# View function to make the recommendation and display to user
def makeRecommenderPageView(request) : 
    # Grab the values from the prediction form
    drug_name = request.POST['drug_name']
    
    # Transform the variable to upper case
    drug_name = drug_name.upper()

    # Query information for the drug
    oDrug = Drug.objects.get(drugname = drug_name)

    # Query information for the Tiple
    oTriple = Triple.objects.all()
    oTriple = oTriple.filter(drug = oDrug.drugid)[1]
    print(oTriple.qty)
    print(oTriple.prescriber_id)
    print(oTriple.drug_id)

    #Query information for the prescriber
    oPrescriber = Prescriber.objects.get(npi = oTriple.prescriber_id)

    import requests
    import json

    url = "http://6d616252-db62-4f9c-be38-6ea57ff8e28a.eastus2.azurecontainer.io/score"

    payload = json.dumps({
    "Inputs": {
        "WebServiceInput2": [
        {
            "drug_id": oTriple.drug_id, #Input the triple information into the web input of our recommender
            "prescriber_id": oTriple.prescriber_id,
            "qty": oTriple.qty
        },
        {
            "drug_id": 221,
            "prescriber_id": 1992883235,
            "qty": 88
        },
        {
            "drug_id": 48,
            "prescriber_id": 1992883235,
            "qty": 76
        }
        ],
        "WebServiceInput0": [
        {
            "npi": oPrescriber.npi,
            "gender": oPrescriber.gender,
            "specialty": oPrescriber.specialty,
            "isopioidprescriber": oPrescriber.isopioidprescriber,
            "totalprescriptions": oPrescriber.totalprescriptions,
        },
        {
            "npi": 1003009630,
            "gender": "M",
            "specialty": "Emergency Medicine",
            "isopioidprescriber": "TRUE",
            "totalprescriptions": 232
        },
        {
            "npi": 1003016270,
            "gender": "M",
            "specialty": "Family Practice",
            "isopioidprescriber": "TRUE",
            "totalprescriptions": 2391
        }
        ],
        "WebServiceInput1": [
        {
            "drugid": oDrug.drugid,
            "isopioid": oDrug.isopioid
        },
        {
            "drugid": 3,
            "isopioid": "True"
        },
        {
            "drugid": 4,
            "isopioid": "False"
        }
        ]
    },
    "GlobalParameters": {}
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer z3zfGUqQ4DA1RrxhkUOHewtfN4RiwPTW'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    obj = json.loads(response.text)

    #Find the prescriber information
    prescriber1 = Prescriber.objects.get(npi = obj['Results']['WebServiceOutput0'][1]['Recommended Item 1'])
    prescriber1 = str(prescriber1.fname) + " " + str(prescriber1.lname)
    prescriber2 = Prescriber.objects.get(npi = obj['Results']['WebServiceOutput0'][1]['Recommended Item 2'])
    prescriber2 = str(prescriber2.fname) + " " + str(prescriber2.lname)
    prescriber3 = Prescriber.objects.get(npi = obj['Results']['WebServiceOutput0'][1]['Recommended Item 3'])
    prescriber3 = str(prescriber3.fname) + " " + str(prescriber3.lname)
    prescriber4 = Prescriber.objects.get(npi = obj['Results']['WebServiceOutput0'][1]['Recommended Item 4'])
    prescriber4 = str(prescriber4.fname) + " " + str(prescriber4.lname)
    prescriber5 = Prescriber.objects.get(npi = obj['Results']['WebServiceOutput0'][1]['Recommended Item 5'])
    prescriber5 = str(prescriber5.fname) + " " + str(prescriber5.lname)

    # Create the output varaibles
    recommendation1 = 'Prescriber 1: ' + prescriber1
    recommendation2 = 'Prescriber 2: ' + prescriber2
    recommendation3 = 'Prescriber 3: ' + prescriber3
    recommendation4 = 'Prescriber 4: ' + prescriber4
    recommednation5 = 'Prescriber 5: ' + prescriber5

    # Pass the output varaibles to the dictionary context that gets passed with the request
    context = {
        "recommendation1" : recommendation1,
        "recommendation2" : recommendation2,
        "recommendation3" : recommendation3,
        "recommendation4" : recommendation4,
        "recommednation5" : recommednation5,
        "drug_name" : drug_name
    }

    return render(request, 'homepages/viewRecommendation.html', context)



# View function to learn more
def learnMorePageView(request) :

    # Get information about who only prescribers opioid
    currentopioidpres = Prescriber.objects.raw("SELECT npi, fname, lname FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True'")
    print(currentopioidpres)

    # How many opioid drugs have been prescribed?
    iNumberPrescribedOpioids = Triple.objects.raw("SELECT SUM(qty) AS Sum FROM pd_triple INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True'")
    iNumberPrescribedOpioids = 31435

    # What opioid drug has been prescribed the most?
    # Query = "SELECT drugname, SUM(qty) AS Total FROM pd_triple INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True' GROUP BY drugname ORDER BY SUM(qty) DESC"
    iNumHydrocodoneAcetaminophen = 21777

    # What state has the most opioid related deaths?
    # Query2 = 'SELECT * FROM pd_statedata ORDER BY deaths DESC LIMIT 1'
    oState = State()
    oState.state = "California"
    oState.deaths = 4521

     # What state has the least opioid related deaths?
    oState2 = State()
    oState2.state = "North Dakota"
    oState2.deaths = 43

    
    context = {
        "currentopioidpres" : currentopioidpres,
        "iNumberPrescribedOpioids" : iNumberPrescribedOpioids,
        "iNumHydrocodoneAcetaminophen" : iNumHydrocodoneAcetaminophen,
        "oState" : oState,
        "oState2" : oState2
    } 
    return render(request, 'homepages/learnmore.html', context)

# View function to display the recommender model
def loginPageView(request) : 
    return render(request, 'homepages/login.html')


# View function to learn more 2 (2 is for vieiwng learn more and index before the login)
def learnMore2PageView(request) :

    # Get information about who only prescribers opioid
    currentopioidpres = Prescriber.objects.raw("SELECT npi, fname, lname FROM pd_prescriber INNER JOIN pd_triple ON pd_prescriber.npi = pd_triple.prescriber_id INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True'")
    print(currentopioidpres)

    # How many opioid drugs have been prescribed?
    iNumberPrescribedOpioids = Triple.objects.raw("SELECT SUM(qty) AS Sum FROM pd_triple INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True'")
    iNumberPrescribedOpioids = 31435

    # What opioid drug has been prescribed the most?
    # Query = "SELECT drugname, SUM(qty) AS Total FROM pd_triple INNER JOIN pd_drugs ON pd_triple.drug_id = pd_drugs.drugid WHERE isopioid = 'True' GROUP BY drugname ORDER BY SUM(qty) DESC"
    iNumHydrocodoneAcetaminophen = 21777

    # What state has the most opioid related deaths?
    # Query2 = 'SELECT * FROM pd_statedata ORDER BY deaths DESC LIMIT 1'
    oState = State()
    oState.state = "California"
    oState.deaths = 4521

     # What state has the least opioid related deaths?
    oState2 = State()
    oState2.state = "North Dakota"
    oState2.deaths = 43

    
    context = {
        "currentopioidpres" : currentopioidpres,
        "iNumberPrescribedOpioids" : iNumberPrescribedOpioids,
        "iNumHydrocodoneAcetaminophen" : iNumHydrocodoneAcetaminophen,
        "oState" : oState,
        "oState2" : oState2
    } 
    return render(request, 'homepages/learnmore2.html', context)