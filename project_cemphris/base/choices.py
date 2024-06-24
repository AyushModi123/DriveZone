from django.db import models

class ProfileCompletionLevelChoices(models.IntegerChoices):
    '''
    Values signifies percentage.
    Adjust values to add more levels.
    '''
    BASIC= 1
    INTERMEDIATE = 2
    COMPLETE = 3


class LicenseTypeChoices(models.IntegerChoices):
    LEARNER = 1 #"Learner's License"
    LMV = 2 #"Light Motor Vehicle License"
    TRANSPORT = 3 #"Transport Vehicle License"
    HMV = 4 #"Heavy Motor Vehicle License"
    HAZARDOUS = 5 #"Hazardous Goods License"
    MOTORCYCLE = 6 #"Motorcycle License"
    TRACTOR = 7 #"Tractor License"
    NTV = 8 #"Non-Transport Vehicle License"
    IDP = 9 #"International Driving Permit"

class LicenseIssuingAuthorityChoices(models.IntegerChoices):
    STATE_TRANSPORT_DEPARTMENT = 1 #"State Transport Department"
    REGIONAL_TRANSPORT_OFFICE = 2 #"Regional Transport Office (RTO)"
    UT_TRANSPORT_DEPARTMENT = 3 #"Union Territory Transport Department"
    MINISTRY_OF_ROAD_TRANSPORT_AND_HIGHWAYS = 4 #"Ministry of Road Transport and Highways (MoRTH)"

class RoleChoices(models.TextChoices):
    LEARNER = 'learner', 'Learner'
    INSTRUCTOR = 'instructor', 'Instructor'
    SCHOOL = 'school', 'School'