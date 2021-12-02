# Import the django.url and views function
from django.urls import path
from .views import indexPageView
from .views import drugLibraryPageView, prescribersPageView, drugDetailsPageView, deletePageView
from .views import viewPrescriberPageView, filterPrescriberPageView, addPrescriberPageView, filterDrugPageView, editPrescriberPageView, updatePrescriberPageView


# Create the different path for index and about 
urlpatterns = [
    path("", indexPageView, name="index"),    
    path("druglibrary/", drugLibraryPageView, name="druglibrary"), # route for the drug library
    path("prescribers/", prescribersPageView, name="prescribers"), # route for the prescriber library
    path("showdrugs/<int:drug_id>", drugDetailsPageView, name='showDrugs'), # route for the drug details
    path("viewprescribers/<int:prescriber_id>", viewPrescriberPageView, name="viewPrescriber"), # route to view the prescriber details
    path("filterprescriber/", filterPrescriberPageView, name="filterprescriber"), # route for the filter prescriber details 
    path("addPrescriber/", addPrescriberPageView, name="addPrescriber"), # route for the filter prescriber details
    path("filterdrug/", filterDrugPageView, name="filterdrug"),  # route for the filter drug details     
    path("editPrescriber/<int:prescriber_id>", editPrescriberPageView, name="editPrescriber"),   
    path("updatePrescriber/", updatePrescriberPageView, name="updatePrescriber"),
    path("delete/<int:prescriber_id>", deletePageView, name="delete"),     
 
]

