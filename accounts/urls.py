from django.urls import path
from .views import Login, Signup, Logout, ForgetPassword, CheckPassword, Dashboard, ResetPassword, SignupDoctor, NotificationsSeen, UpdateProfile,ConfirmDoctorProfile


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
    path('forgetpassword/', ForgetPassword.as_view(), name='forgetpassword'),
    path('checkpassword/', CheckPassword.as_view(), name='checkpassword'),
    path('resetpassword/', ResetPassword.as_view(), name='resetpassword'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('update/profile/', UpdateProfile.as_view(), name='updateprofile'),

    #Personal URLs
    path('signup/doctor/', SignupDoctor.as_view(), name='singup_doctor'),
    path('confirm/doctor/', ConfirmDoctorProfile.as_view(), name='confirm_doctor'),

    #Notifications URLs
    path('notifications/seen', NotificationsSeen.as_view(), name='seen_notifications'),

]
