#built in django module
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Sum
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


#built in python
import random

#modules from current directory
from .models import CustomUser, Notifications, Doctor, Specialty, SubSpecialty
from .forms import LoginForm, SignupForm, ForgetPasswordForm, CheckPasswordForm, ResetPasswordForm, UpdateProfileForm, UpdateDoctorForm

#modules from other app
from main.models import State, City

class Login(View):
    def get(self,request):
        #if user was logged in, then redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = LoginForm()

        context = {
            'form' : form,
        }

        return render(request, 'accounts/login.html', context)
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            #get cleaned data
            data = form.cleaned_data
            password = data['password']
            national_code = data['national_code']

            #If a user with the entered profile is found
            user = authenticate(request, national_code=national_code,password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, level=messages.SUCCESS, message='خوش آمدید! ورود شما موفقیت آمیز بود.')
                return redirect('dashboard')
            else:
                messages.add_message(request, level=messages.ERROR, message='کاربری با این کدملی و رمز عبور پیدا نشد')
                return redirect('login')
        else:
            context = {
                'form': form
            }
            return render(request, 'accounts/login.html', context)

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main')

class Signup(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = SignupForm()
        context = {
            'form' : form
        }
        return render(request, 'accounts/signup.html', context)
    
    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            #get cleaned data and create user
            user = CustomUser.objects.create_user(national_code=data['national_code'],password=data['password'])
            user.save()

            #If a user with the entered profile is found
            user = authenticate(request, national_code=data['national_code'],password=data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(request, level=messages.SUCCESS, message='حساب شما ایجاد گردید')
                return redirect('dashboard')
            else:
                messages.add_message(request, level=messages.ERROR, message='حساب شما ایجاد گردید. اما برای لاگین کردن بصورت خودکار مشکلی پیش آمد! لطفا وارد حساب خود شوید')
                return redirect('login')
        
        else:
            context = {
                'form' : form,
            }
            return render(request, 'accounts/signup.html', context)


class SignupDoctor(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = SignupForm()
        is_doctor_form = True

        context = {
            'form' : form,
            'is_doctor_form' : is_doctor_form
        }
        return render(request, 'accounts/signup.html', context)
    
    def post(self, request):
        form = SignupForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            #create user profile
            user = CustomUser.objects.create_user(national_code=data['national_code'],password=data['password'])
            user.save()

            #create personal profile
            doctor = Doctor.objects.create(prifle=user)
            doctor.save()

            #If a user with the entered profile is found
            user = authenticate(request, national_code=data['national_code'],password=data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(request, level=messages.SUCCESS, message='حساب شما ایجاد گردید')
                return redirect('confirm_doctor')
            else:
                messages.add_message(request, level=messages.ERROR, message='حساب شما ایجاد گردید. اما برای لاگین کردن بصورت خودکار مشکلی پیش آمد! لطفا وارد حساب خود شوید')
                return redirect('login')
        
        else:
            context = {
                'form' : form,
            }
            return render(request, 'accounts/signup.html', context)
        
        
"""class UpdateProfile(View):
    def post(self, request):
        if request.user.is_authenticated:
            form = UpdateProfileForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                user.username = data['username']
                user.email = data['email']
                user.save()

                messages.add_message(request, messages.SUCCESS, 'پروفایل شما بروزرسانی شد')
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.WARNING, message=form.errors['__all__'])
                return redirect('dashboard')
         """   
class ConfirmDoctorProfile(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateDoctorForm()
            states = State.objects.all()
            cities = City.objects.all()
            specialties = Specialty.objects.all()
            sub_specialties = SubSpecialty.objects.all()

            context = {
                'form' : form,
                'states' : states,
                'cities' : cities,
                'specialties' : specialties,
                'sub_specialties' : sub_specialties,
            }

            return render(request, "accounts/confirm_doctor.html", context)
    
    def post(self, request):
        if request.user.is_authenticated:
            form = UpdateDoctorForm(request.POST)

            if form.is_valid():

                data = form.cleaned_data
                user = CustomUser.objects.get(national_code=request.user.national_code)
                doctor = Doctor.objects.get(profile=user)

                #update user profile
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.email = data['email']
                user.phone = data['phone']
                user.save()

                #update personal profile
                doctor.state = data['state']
                doctor.city = data['city']
                doctor.address = data['address']
                doctor.specialty = data['specialty']
                doctor.sub_specialty = data['sub_specialty']
                doctor.is_active = True
                doctor.save()

                messages.add_message(request, messages.SUCCESS, 'پروفایل شما به عنوان پزشک ایجاد گردید')
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.WARNING, message=form.errors['__all__'])
                return redirect('confirm_doctor')



class ForgetPassword(View):
    def get(self, request):
        form = ForgetPasswordForm()

        context = {
            'form' : form,
        }

        return render(request, 'accounts/forgetpassword.html', context)
    
    def post(self, request):
        form = ForgetPasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = data['email']

            #check user exist
            user = CustomUser.objects.filter(email=email)
            if user:

                user = CustomUser.objects.get(email=email)

                #create 6 digits random number for generate a confirm code
                numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                confirm_code = ''
                for i in range(6):
                    confirm_code += random.choice(numbers)

                #confirm code and user email save in these sessions for keeping detail of user 
                request.session['confirm_code'] = confirm_code
                request.session['email_address'] = data['email']

                #send confirm code to user email
                subject = 'فراموشی رمز عبور'
                message = f'کد شما: {confirm_code} \n\n این کد یکبار مصرف و تا 9 دقیقه دیگر اعتبار خواهد داشت. \n\n === Persian-Petshop ==='
                email_from = settings.EMAIL_HOST_USER
                email_to = [data['email']]

                send_mail(subject, message, email_from, email_to)
                return redirect('checkpassword')

            else:
                messages.add_message(request, messages.WARNING, 'اکانتی با این ایمیل پیدا نشد!')
                return redirect('forgetpassword')
        else:
            context = {
                'form' : form
            }
            return render(request, 'accounts/forgetpassword.html', context)


class CheckPassword(View):
    def get(self, request):
        if request.session['confirm_code']:
            form = CheckPasswordForm()

            context = {
                'form' : form,
            }

            return render(request, 'accounts/checkpassword.html', context)
        else:
            return redirect('forgetpassword')
    
    def post(self, request):
        form = CheckPasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            
            #if entered confirm code equal with confirm code of stored in session
            if request.session['confirm_code'] == data['check_code']:
                del request.session['confirm_code']

                return redirect('resetpassword')
            else:
                context = {
                    'form' : form,
                }
                messages.add_message(request, messages.ERROR, 'کد وارد شده با کدی که برای شما ارسال گردیده است مطابقت ندارد')
                return render(request, 'accounts/checkpassword.html', context)
        else:
            context = {
                'form' : form
            }
            return render(request, 'accounts/checkpassword.html', context)
        

class ResetPassword(View):
    def get(self, request):
        try:
            form = ResetPasswordForm()
            context = {
                'form' : form,
            }
            return render(request, 'accounts/resetpassword.html', context)
        except:
            return redirect('forgetpassword')
    
    def post(self, request):
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                #get user profile with email address for change the password
                email = request.session['email_address']
                user = CustomUser.objects.get(email=email)
                user.set_password(data['password'])
                user.save()

                del request.session['email_address']

                messages.add_message(request, messages.SUCCESS, 'رمز عبور شما با موفقیت تغییر گردید. اکنون وارد حساب خود شوید')
                return redirect('login')
            except:
                messages.add_message(request, messages.WARNING, 'در بازنشانی گذرواژه مشکلی بوجود آمد. دوباره امتحان کنید')
                return redirect('forgetpassword')
        else:
            context = {
                 'form' : form,
            }
            return render(request, 'accounts/resetpassword.html', context)


class Dashboard(View):
    def get(self, request):
        #check user logged in
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, 'ابتدا وارد حساب کاربری خود شوید')
            return redirect('login')
        
        #if the user was admin
        if request.user.is_superuser:

            return render(request, 'accounts/dashboard.html', context)
        else:
            #get profile user
            user = request.user

            #if there was a personal with that profile
            doctor = Doctor.objects.filter(profile=user)

            #get notifications
            notifications = Notifications.objects.filter(send_to=user, status='Unseen')

            context = {
                'user' : user,
                'notifications' : notifications,
            }

            
            #if user was a personal by "Verified" status
            if doctor:
                if doctor[0].is_active == True:      
                    messages.add_message(request, messages.SUCCESS, 'You are a doctor')
            
            return render(request, 'accounts/dashboard.html', context)
    
    def post(self, request):

        #if user was a superuser
        if request.user.is_superuser:
            pass
        else:
            pass
        


#Notifications
class NotificationsSeen(View):
    def get(self, request):
        user = request.user
        notifications = Notifications.objects.filter(send_to=user)

        for notif in notifications:
            notif.status = 'Seen'
            notif.save()
        
        return redirect('dashboard')