from django.shortcuts import redirect, render
from .models import Alloted_Beds, Appointment, Birth_report, Department, Donors, Medicine, Medicine_log, Patient, Roomlog,staff_type
from django.contrib.auth import authenticate,login,logout
from .forms import NewUserForm
from datetime import datetime
from django.contrib.auth.models import User



#This view is responsible for loging the user into the management system 
def welcome_page(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request,username=username,password=password)
       if user is not None:
           login(request,user)
           return redirect('dashboard')
    return render(request,'management/Pages/login_page.html')

# This view is responsible for creating a new user instance
def sign_up_page(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('update_user_profile') 
    form = NewUserForm()   
    context = {
        'form':form
    }
    return render(request,'management/Pages/signup_page.html',context)

def dashboard(request):
    if request.user.is_staff:
        STAFF_OBJ = staff_type.objects.get(user = request.user)
        dtnw = datetime.now()
        dt = f"{dtnw.date()}T{dtnw.hour}:{'%02d' % (dtnw.minute)}:00"
        patobj = Patient.objects.all()
        aptobj = Appointment.objects.all()
        pp = staff_type.objects.get(user = request.user).Profile_image.url
        available_doctors = staff_type.objects.filter(type = "D")

        context = {"available_doctors" : available_doctors,"patients" : patobj,"dtnw":dt, "appointments": aptobj,"pp" : pp }
        
        if STAFF_OBJ.type == "R" :
            if request.session.get('_old_post'):
                context['response'] = request.session.get('_old_post')
                del request.session['_old_post']
            return render(request, 'management/Pages/dashboard-reception.html', context)
        
        elif STAFF_OBJ.type == "N" :
            return render(request, 'management/Pages/dashboard-nurse.html', context)
    else:
        return redirect(request,"login_page")


def check_patient(request):
    if request.method == 'POST':
        try:
            Patient.objects.get(Patient_lastname = request.POST['lname'],Patient_firstname = request.POST['fname'],Patient_email_address = request.POST['email'])
            request.session['_old_post'] = 'Patient instance already exists'
            return redirect('/management/dashboard')
        except:
            return render(request,'management/Pages/add_patient.html')

def book_appointment(request):
    if request.user.is_staff:
        if request.method == "POST":
            Appointment.objects.create(
                Patient = Patient.objects.get(id = request.POST['selpat']) ,
                Appointment_start_date = request.POST['date-time'],
                Assigned_doctor = User.objects.get(id = request.POST['seldoct']),
                Reason_for_Appointment = request.POST['reason'],
            )
        return redirect(request.POST['backlink'])

def administered(request):
    if request.user.is_staff:
        context = {"administered_patient" : Roomlog.objects.filter(checkout_time__isnull = True),"drugs":Medicine_log.objects.all()}
        return render(request, "management/Pages/administered_patient.html", context)

def logout_user(request):
    logout(request)
    return redirect('login_page')