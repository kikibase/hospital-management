from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseServerError

# Create your models here.

class staff_type(models.Model):#only if staff
    staff_types =   [
        ('R' ,'RECEPTION'),
        ('N' , 'NURSE'),
        ('D' , 'DOCTOR'),
        ('P' , 'PHARMACY'),
        ('L' , 'LAB'),
        ('A' , 'ACCOUNT'),
    ]
    
                    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=200 ,choices= staff_types)
    Profile_image = models.ImageField(blank=True, null=True,default="Null")
    phone_number = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    specialization = models.CharField(max_length=200, default="none")#used mostly for doctors with specialized fields
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=200)#THe wing and room


class Department(models.Model):
    Department_name = models.CharField(max_length=250, unique=True, blank=True, null=True)
    Department_details = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.Department_name + " Department"

class Room(models.Model):
    Room_location = models.CharField(max_length=250, null=True,blank=True)
    Room_NUMBER = models.CharField(max_length=100, null=True, blank=True, unique=True)
    


    def __str__(self):
        return "Located at :" + self.Room_location 

GENDER = (
        ('UNDECIDED','UNDECIDED'),
        ('MALE','MALE'),
        ('FEMALE','FEMALE')
    )



class Patient(models.Model):
    Patient_lastname = models.CharField(max_length=250,null=True, blank=True)
    Patient_firstname = models.CharField(max_length=250,null=True, blank=True)
    Patient_email_address = models.EmailField(max_length=250, null=True, blank=True)
    Patient_phone_number = models.CharField(max_length=120, null=True, blank=True)
    Patient_address = models.CharField(max_length=350,null=True,blank=True)
    Patient_blood_group = models.CharField(max_length=200)
    Patient_blood_genotype = models.CharField(max_length=200)
    Patient_age = models.IntegerField()
    Patient_gender = models.CharField(max_length=25, choices=GENDER,default="UNDECIDED")

    def __str__(self):
        return self.Patient_lastname +" " + self.Patient_firstname + " Details"

class Bill(models.Model):
    PAYMENT_STATUS = (
        ("PENDING","PENDING"),
        ("COMPLETED","COMPLETED"),
    )

    patient_name = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank= True)
    amount_paid = models.FloatField(max_length=2000)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="PENDING")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name.Patient_lastname + "PAYMENT STATUS IS " + self.payment_status

class Appointment(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.PROTECT)
    Appointment_start_date = models.DateTimeField()
    Appointment_end_date = models.DateTimeField()
    Assigned_doctor = models.ForeignKey(User,on_delete=models.PROTECT)
    Reason_for_Appointment = models.TextField(max_length=2500)
    Appointment_status = models.CharField(max_length=200,choices=(("A","active"),("W","waiting"),("C","cancelled"),("F","finished")),default="W")


    def __str__(self):
        return self.Fullname + " Appointment"

    def save(self, *args, **kwargs) -> None: #when creating reference, ensure that the refernce is unique
        S = staff_type.objects.get(user = self.Assigned_doctor)
        if S != "D":
            raise HttpResponseServerError

        super().save(*args, **kwargs)

    

class Alloted_Beds(models.Model):
    Room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True, blank=True)
    Bed_number = models.IntegerField()


class Roomlog(models.Model):
    Room=models.ForeignKey(Room,on_delete=models.PROTECT)
    Bed = models.ForeignKey(Alloted_Beds, on_delete=models.PROTECT)
    Patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(null=True, blank = True)

    def __str__(self):
        return f"Room: {self.Room.ROOM_NUMBER} at {self.Room.ROOM_LOCATION} is logged by {self.Patient.Patient_lastname} {self.Patient.Patient_firstname} between {self.checkin_time} to {(self.checkout_time if self.checkout_time is not None else 'present')} "    


class Medicine(models.Model):
    name = models.CharField(max_length=250)
    quantity_available = models.IntegerField()
    nafdac_no = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.name + " Drug Details"

class Donors(models.Model):
    name = models.CharField(max_length=250)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=250)
    bloood_genotype = models.CharField(max_length=250)
    donor_contact = models.CharField(max_length=250,default="Please Update")
    date_donated = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    amount_donated = models.CharField(null=True, max_length=250,blank=True)

    def __str__(self):
        return self.name + " Blood"

    def calculate_age(self):
        patient_age = self.date_of_birth - self.date_donated
        return patient_age

class Operation(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,max_length=250)
    description = models.TextField(max_length=2048, null=True, blank=True)
    doctor = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    emergency = models.BooleanField(default=False)
    
    def __str__(self):
        return self.patient.Patient_lastname + self.patient.Patient_firstname + " Operation Details"

    def save(self, *args, **kwargs) -> None: #when creating reference, ensure that the refernce is unique
        S = staff_type.objects.get(user = self.Assigned_doctor)
        if S != "D":
            raise HttpResponseServerError

        super().save(*args, **kwargs)
    

class Birth_report(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True, blank=True)
    description = models.TextField(max_length=2048, null=True,blank=True)
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    mode_of_delivery = models.CharField(max_length=250,null=True, blank=True)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.Patient_lastname + self.patient.Patient_firstname + " Birth Report"

    def save(self, *args, **kwargs) -> None: #when creating reference, ensure that the refernce is unique
        S = staff_type.objects.get(user = self.Assigned_doctor)
        if S != "D":
            raise HttpResponseServerError

        super().save(*args, **kwargs)

