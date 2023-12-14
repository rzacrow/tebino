from django.db import models
from django.contrib.auth.models import User, AbstractUser
from main.models import State, City
class CustomUser(AbstractUser):
    national_code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=11, blank=False, null=False)
    
    REQUIRED_FIELDS = ['national_code', 'password', 'phone', 'first_name', 'last_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" 

class Specialty(models.Model):
    SPECIALTY_CHOICES = (
        ('1', 'متخصص بیهوشی'),
        ('2', 'استخوان و ارتوپد'),
        ('3', 'خون، سرطان و آنکولوژی'),
        ('4', 'آزمایشگاه و تصویربرداری'),
        ('5', 'ریه و دستگاه تنفسی'),
        ('6', 'کلیه و مجاری ادراری'),
    )
    title = models.CharField(max_length=1, blank=False, null=False, unique=True, choices=SPECIALTY_CHOICES)

    def __str__(self) -> str:
        return self.title

class SubSpecialty(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    title = models.CharField(max_length=2, blank=False, null=False, unique=True)

    def __str__(self) -> str:
        return self.title

class Doctor(models.Model):
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    sub_specialty = models.ForeignKey(SubSpecialty, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=False, null=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False)

class SCORE(models.Model):
    COUNT_SCORE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    SCORE_TITLE = (
        ('B', 'Behavior'),
        ('S', 'Skill'),
        ('O', 'Ontime'),
    )
    
    title = models.CharField(choices=SCORE_TITLE, max_length=1, null=True, )
    score = models.SmallIntegerField(choices=COUNT_SCORE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    text = models.CharField(max_length=555, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.doctor.profile.first_name} {self.doctor.profile.last_name}"