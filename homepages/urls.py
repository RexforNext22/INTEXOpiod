# Import the django.url and views function
from django.urls import path
from .views import indexPageView
from .views import drugLibraryPageView, prescribersPageView, drugDetailsPageView
from .views import viewPrescriberPageView, filterPrescriberPageView, addPrescriberPageView


# Create the different path for index and about 
urlpatterns = [
    path("", indexPageView, name="index"),    
    path("druglibrary/", drugLibraryPageView, name="druglibrary"), # route for the drug library
    path("prescribers/", prescribersPageView, name="prescribers"), # route for the prescriber library
    path("showdrugs/<int:drug_id>", drugDetailsPageView, name='showDrugs'), # route for the drug details
    path("viewprescribers/<int:prescriber_id>", viewPrescriberPageView, name="viewPrescriber"), # route to view the prescriber details
    path("filterprescriber/", filterPrescriberPageView, name="filterprescriber"), # route for the filter prescriber details 
    path("addPrescriber/", addPrescriberPageView, name="addPrescriber"), # route for the filter prescriber details           
]

