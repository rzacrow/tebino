from django.db import models
from accounts.models import Doctor, CustomUser

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    count = models.IntegerField(blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.doctor.profile.first_name} {self.doctor.profile.last_name}"

class AppointmentBooked(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time = models.TimeField()
    tracking_code = models.IntegerField(blank=False, null=False, unique=True)

    def __str__(self) -> str:
        return self.tracking_code
