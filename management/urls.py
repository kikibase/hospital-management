from django.urls import path
from management import views
urlpatterns = [ 
    path('', views.welcome_page,name="login_page"),
    path('create_account/', views.sign_up_page,name="signup_page"),
    path('doctors/',views.doctors_page, name="doctors_page"),
    path('departments/',views.departments_page, name="departments_page"),
    path('patients/',views.patient_page, name="patients_page"),
    path('patients/<str:pk>',views.patient_details_page,name="detailed_patient_page"),
    path('financies/',views.financial_activities, name="financies_page"),
    path('medicines/',views.medicines, name="medicine_page"),
    path('donors/',views.donors_page, name="donors_page"),
    path('beds/',views.beds_page, name="beds_page"),
    path('reports/',views.reports_page, name="reports_page"),
    path('profile_page/',views.profile_page, name="profile_page"),
    path('nurse_profile_page/', views.nurse_profile,name="nurse_profile"),
    path('update_doctor_profile/<int:pk>/',views.update_user_profile,name="update_profile"),
    path('update_nurse_profile/<int:pk>/',views.update_nurse_profile,name="update_profile"),
    path('logout_user/',views.logout_user, name="logout"),
    #Okiki starts here
    path('dashboard/',views.dashboard, name="dashboard"),
    path('check_patient/',views.check_patient, name="check_patient"),
    path('book_appointment/',views.book_appointment),
]