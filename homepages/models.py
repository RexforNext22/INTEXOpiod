from django.db import models

# Create your models here.

#Model for statedata
class State(models.Model):
    state = models.CharField(max_length=10, blank=True, unique=True) #This value has to be unique, cannot be duplicated
    stateabbrev = models.CharField(max_length=2, blank=True, primary_key=True, unique=True) #This value has to be unique, cannot be duplicated
    population = models.IntegerField(default=0, blank=True)
    deaths = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table = "pd_statedata"

    def __str__(self):
        return self.state # the discription will be seen on the admin page

# Model for Prescriber
class Prescriber(models.Model):
    npi = models.IntegerField(default=0, blank=True, primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    state = models.ForeignKey(State, to_field="stateabbrev", on_delete = models.DO_NOTHING, default='',verbose_name="State")
    credentials = models.CharField(max_length=30)
    specialty = models.CharField(max_length=62)
    isopioidprescriber = models.CharField(max_length=5)
    totalprescriptions = models.IntegerField(default=0, blank=True)



    class Meta:
        db_table = "pd_prescriber"

    def __str__(self):
        return self.fname + ' ' + self.lname # the discription will be seen on the admin page
#Model for pd-drugs
class Drug(models.Model):
    drugid = models.IntegerField(blank=True, primary_key=True, unique=True) 
    drugname = models.CharField(max_length=30, unique=True)
    isopioid = models.CharField(max_length=5)

    class Meta:
        db_table = "pd_drugs"

    def __str__(self):
        return self.drugname # the discription will be seen on the admin page

#Model for pd_triple
class Triple(models.Model):
    prescriber_id = models.ForeignKey(Prescriber, to_field="npi", on_delete=models.DO_NOTHING, default='', verbose_name="Prescriber")
    drugid = models.ForeignKey(Drug, to_field="drugid", on_delete=models.DO_NOTHING, default='', verbose_name="Drugs")
    qty = models.IntegerField(default=0, blank=True)
    
    class Meta:
        db_table = "pd_triple"

    def __str__(self):
        return str(self.drugname) # the discription will be seen on the admin page

