from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Room)
admin.site.register(Alloted_Beds)
admin.site.register(Medicine)
admin.site.register(Donors)
admin.site.register(Birth_report)
admin.site.register(Appointment)
admin.site.register(staff_type)

