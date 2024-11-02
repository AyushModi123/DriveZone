from django.contrib import admin

from .models import User, Learner, Instructor, LicenseInformation, School, ActivationMailHistory

admin.site.register(User)
admin.site.register(School)
admin.site.register(Learner)
admin.site.register(Instructor)
admin.site.register(LicenseInformation)
admin.site.register(ActivationMailHistory)
