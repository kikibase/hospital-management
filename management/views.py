from django.http import Http404
from django.shortcuts import redirect, render
from .models import Appointment, Medicine, Medicine_log, Patient, Patient_medical_log, Room, Roomlog,staff_type
from django.contrib.auth import authenticate,login,logout
from .forms import NewUserForm
from datetime import datetime
from django.contrib.auth.models import User



#This view is responsible for loging the user into the management system 
def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        sesslog = request.session.get('login-error')
        if sesslog:
            context = {"loginerr" : sesslog}
            del request.session['login-error']
            return render(request,'management/Pages/login_page.html', context)
        return render(request,'management/Pages/login_page.html')

def login_l(request):
    if request.method == 'POST':
        if request.POST['email-username'].find('@') >= 0:
            username = User.objects.get(email = request.POST['email-username']).username
            password = request.POST['password']
        else:
            username = request.POST['email-username']
            password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            request.session['login-error'] = 'username/email or password is wrong'
            return redirect('login_page')
    else:
        raise Http404

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
        
        elif STAFF_OBJ.type == "D" :
            return render(request, 'management/Pages/dashboard-doc.html', context)

        elif STAFF_OBJ.type == "P" :
            return render(request, 'management/Pages/dashboard-pharmacy.html', context)

    else:
        return redirect("login_page")


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
        context = {"administered_patient" : Roomlog.objects.filter(checkout_time__isnull = True),"drugs":Medicine_log.objects.filter(room__isnull = False)}
        return render(request, "management/Pages/administered_patient.html", context)


def patient_info(request):
    if request.user.is_staff:
        if request.method == 'POST':
            cont = []
            for val in Patient.objects.filter(Patient_firstname__contains = request.POST['search']):
                cont.append(val)
            for val in Patient.objects.filter(Patient_lastname__contains = request.POST['search']):
                if cont.count(val)<=1:
                    cont.append(val)
            for val in Patient.objects.filter(Patient_email_address__contains = request.POST['search']):
                if cont.count(val)<=1:
                    cont.append(val)
            for val in Patient.objects.filter(Patient_phone_number__contains = request.POST['search']):
                if cont.count(val)<=1:
                    cont.append(val)
            
            context = {"search_result" : cont }
            return render(request, "management/Pages/patient_info.html", context)
        else:
            context = {"search_result": Patient.objects.all()}
            return render(request, "management/Pages/patient_info.html", context)


def patient_full_info(request,pk):
    if request.user.is_staff:
        rmfil =[]
        bdfil = []
        for s in Room.objects.all():
            rmfil.append(s)
        for d in Roomlog.objects.filter(checkout_time__isnull = True):
            rmfil.remove(d)


        context = {
            'pt' : Patient.objects.get(id = pk),
            'ptlogs':Patient_medical_log.objects.filter(patient_id = pk ),
            'drlogs' : Medicine_log.objects.filter(patient_id = pk),
            'dr': Medicine.objects.all(),
            'rm' : rmfil,
            'rmbd':bdfil
            }
        return render(request, "management/Pages/pfl.html", context )


def bkroom(request):
    if request.method=='POST':
       #Roomlog.objects.create(
       #    Room_id= ,
       #    Bed =,
       #    Patient =   ,
       #)
       return None




        

def logout_user(request):
    logout(request)
    return redirect('login_page')