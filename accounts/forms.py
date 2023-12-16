from django import forms
from django.core.exceptions import ValidationError
#from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import CustomUser
import pandas as ps


class LoginForm(forms.Form):
    national_code = forms.CharField(max_length=255, required=True, label=None, strip=True)
    password = forms.CharField(max_length=16, required=True, label=None, strip=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['national_code'].widget.attrs['placeholder'] = 'کد ملی'
        self.fields['password'].widget.attrs['placeholder'] = 'گذرواژه'

class SignupForm(forms.Form):
    national_code = forms.CharField(max_length=255, required=True, label=None, strip=True)
    password = forms.CharField(max_length=16, required=True, label=None, strip=True, widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['national_code'].widget.attrs['placeholder'] = 'کد ملی'
        self.fields['password'].widget.attrs['placeholder'] = 'گذرواژه'


    def clean(self):
        cleaned_data = super().clean()
        national_code = cleaned_data.get('national_code')
        password = cleaned_data.get('password')

        
        if (national_code == None) or (password == None):
            raise ValidationError('این فیلد حتما باید دارای مقدار باشد')
            
        if len(password) < 8:
            raise ValidationError('رمز عبور شما باید 8 کاراکتر و یا بیشتر باشد.')
        
    def clean_national_code(self):
        national_code = self.cleaned_data['national_code']
        if CustomUser.objects.filter(national_code=national_code).exists():
            raise forms.ValidationError('حسابی با این کد ملی از قبل ایجاد شده است')
        return national_code



class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=16, required=True, strip=True, widget=forms.PasswordInput, label='گذرواژه')
    repassword = forms.CharField(max_length=16, required=True, strip=True, widget=forms.PasswordInput, label='تکرار گذرواژه')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')

        if len(password) < 8:
            raise ValidationError('رمز عبور شما باید 8 کاراکتر و یا بیشتر باشد.')
            
        if password != repassword:
            raise ValidationError('رمز عبور با تکرار آن باید یکی باشد.')


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True, label='ایمیل')


class CheckPasswordForm(forms.Form):
    check_code = forms.CharField(max_length=6, required=True, strip=True, label='کد تایید')




class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True, label=None, strip=True)
    last_name = forms.CharField(max_length=255, required=True, label=None, strip=True)
    email = forms.EmailField(max_length=255, required=True, label=None)
    phone = forms.CharField(max_length=11, required=True, label=None, strip=True)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی'
        self.fields['email'].widget.attrs['placeholder'] = 'ایمیل'
        self.fields['phone'].widget.attrs['placeholder'] = 'تلفن'
    

class UpdateDoctorForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True, label=None, strip=True)
    last_name = forms.CharField(max_length=255, required=True, label=None, strip=True)
    email = forms.EmailField(max_length=255, required=True, label=None)
    phone = forms.CharField(max_length=11, required=True, label=None, strip=True)
    address = forms.CharField(max_length=255, required=True, label="آدرس", strip=True)


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی'
        self.fields['email'].widget.attrs['placeholder'] = 'ایمیل'
        self.fields['phone'].widget.attrs['placeholder'] = 'تلفن'