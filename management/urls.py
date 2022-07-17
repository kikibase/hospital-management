from django.urls import path
from management import views
urlpatterns = [ 
    path('login/', views.login_l,name="nigol"),
    path('logout/', views.logout_user,name="logout"),
    path('', views.login_page,name="login_page"),
    path('create_account/', views.sign_up_page,name="signup_page"),
    path('logout_user/',views.logout_user, name="logout"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('check_patient/',views.check_patient, name="check_patient"),
    path('book_appointment/',views.book_appointment),
    path('administered/',views.administered),
    path('patient_info/',views.patient_info),
    path('p-f-l/<str:pk>/',views.patient_full_info),
]