from django.contrib import admin

from .models import User, Learner, Instructor, LicenseInformation

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(Instructor)
admin.site.register(LicenseInformation)

