from django.db import models

# Create your models here.

#Model for statedata
class StateData(models.Model):
    state = models.CharField(max_length=10, blank=True, unique=True) #This value has to be unique, cannot be duplicated
    stateabbrev = models.CharField(max_length=2, blank=True)
    population = models.IntegerField(default=0, blank=True)
    deaths = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table = "pd_statedata"

    def __str__(self):
        return self.state # the discription will be seen on the admin page

#Model for Prescriber
class Prescriber(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    state = models.ForeignKey(StateData, on_delete=models.DO_NOTHING, default='', verbose_name="State")
    credentials = models.CharField(max_length=30)
    specialty = models.CharField(max_length=62)
    is_opioid_prescriber = models.BooleanField()
    total_prescriptions = models.IntegerField(default=0, blank=True)



    class Meta:
        db_table = "pd_prescriber"

    def __str__(self):
        return self.first_name + ' ' + self.last_name # the discription will be seen on the admin page
#Model for pd-drugs
class Drugs(models.Model):
    drugname = models.CharField(max_length=30)
    is_opioid = models.BooleanField()

    class Meta:
        db_table = "pd_drugs"

    def __str__(self):
        return self.drugname # the discription will be seen on the admin page
        
#Model for pd_triple
class Triple(models.Model):
    prescriber_id = models.ForeignKey(Prescriber, on_delete=models.DO_NOTHING, default='', verbose_name="Prescriber")
    drugname = models.ForeignKey(Drugs, on_delete=models.DO_NOTHING, default='', verbose_name="Drugs")
    quantity = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table = "pd_triple"

    def __str__(self):
        return self.drugname # the discription will be seen on the admin page

