from django.urls import path
from management import views
urlpatterns = [ 
    path('', views.welcome_page,name="login_page"),
    path('create_account/', views.sign_up_page,name="signup_page"),
    path('logout_user/',views.logout_user, name="logout"),
    #Okiki starts here
    path('dashboard/',views.dashboard, name="dashboard"),
    path('check_patient/',views.check_patient, name="check_patient"),
    path('book_appointment/',views.book_appointment),
    path('administered/',views.administered),
    path('patient_info/',views.patient_info),
]