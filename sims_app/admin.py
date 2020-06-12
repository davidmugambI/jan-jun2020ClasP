from django.contrib import admin
from sims_app.models import Course,Student,Application

# Register your models here.
admin.site.register([Course,Student,Application])