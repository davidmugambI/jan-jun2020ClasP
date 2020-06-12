from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
class Course(models.Model):
    Course_Name = models.CharField(max_length=50)
    Course_Duration = models.IntegerField()
    Course_Fee = models.DecimalField(max_digits=7,decimal_places=2) # e.g 36000.00
    CreatedOn = models.DateTimeField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.Course_Name

class Student(models.Model):
    Reg_No = models.CharField(max_length=20)  # ZAL/2020/1
    First_Name = models.CharField(max_length=20)
    Last_Name = models.CharField(max_length=20)
    Surname = models.CharField(max_length=20)
    Email = models.EmailField()

    # phone number regular expression
    phone_number_validator = RegexValidator(regex=r'^(0|\+)\d{8,15}$')

    Phone_Number = models.CharField(validators=[phone_number_validator],max_length=17,unique=True)
    EnrolledOn = models.DateTimeField(auto_now_add=True)
    Cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.First_Name + " " + self.Last_Name

class Application(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    EnrolledOn = models.DateTimeField(auto_now_add=True)
    Expired = models.BooleanField(default=False)

    def __str__(self):
        return  self.student.Reg_No

"""
Repeating columns in a database - Redundancy
Handling redundancy - Normalization
"""