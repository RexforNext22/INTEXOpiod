# Import the django.url and views function
from django.urls import path
from .views import indexPageView
from .views import drugLibraryPageView, prescribersPageView 
from .views import drugDetailsPageView, deletePageView, additionPrescriberPageView, predictionPageView, makePredictionPageView
from .views import viewPrescriberPageView, filterPrescriberPageView, addPrescriberPageView 
from .views import filterDrugPageView, editPrescriberPageView, updatePrescriberPageView


# Create the different path for index and about 
urlpatterns = [
    path("", indexPageView, name="index"),    
    path("druglibrary/", drugLibraryPageView, name="druglibrary"), # route for the drug library
    path("prescribers/", prescribersPageView, name="prescribers"), # route for the prescriber library
    path("showdrugs/<int:drug_id>", drugDetailsPageView, name='showDrugs'), # route for the drug details
    path("viewprescribers/<int:prescriber_id>", viewPrescriberPageView, name="viewPrescriber"), # route to view the prescriber details
    path("filterprescriber/", filterPrescriberPageView, name="filterprescriber"), # route for the filter prescriber details 
    path("addPrescriber/", addPrescriberPageView, name="addPrescriber"), # route for the filter prescriber details
    path("additionprescriber/", additionPrescriberPageView, name="additionprescriber"), # route for the filter prescriber details
    path("filterdrug/", filterDrugPageView, name="filterdrug"),  # route for the filter drug details     
    path("editPrescriber/<int:prescriber_id>", editPrescriberPageView, name="editPrescriber"), # route to show the edit prescriber view function  
    path("updatePrescriber/", updatePrescriberPageView, name="updatePrescriber"), # route to update the prescriber profile
    path("delete/<int:prescriber_id>", deletePageView, name="delete"), # route to delete the prescribe profile
    path("prediction/", predictionPageView, name="prediction"),  # route to see the prediction model
    path("makePrediction/", makePredictionPageView, name="makePrediction"), # route to run the prediction model     
 
]

