# Import the django.url and views function
from django.urls import path
from .views import indexPageView
from .views import drugLibraryPageView


# Create the different path for index and about 
urlpatterns = [
    path("", indexPageView, name="index"),    
    path("druglibrary/", drugLibraryPageView, name="druglibrary"),   
]