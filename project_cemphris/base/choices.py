from django.db import models

class ProfileCompletionLevelChoices(models.IntegerChoices):
    '''
    Values signifies percentage.
    Adjust values to add more levels.
    '''
    BASIC= 1
    INTERMEDIATE = 2
    COMPLETE = 3


class LicenseTypeChoices(models.TextChoices):
    LEARNER = ('learner', "Learner's License")
    LMV = ('lmv', "Light Motor Vehicle License")
    TRANSPORT = ('transport', "Transport Vehicle License")
    HMV = ('hmv', "Heavy Motor Vehicle License")
    HAZARDOUS = ('hazardous', "Hazardous Goods License")
    MOTORCYCLE = ('motorcycle', "Motorcycle License")
    TRACTOR = ('tractor', "Tractor License")
    NTV = ('ntv', "Non-Transport Vehicle License")
    IDP = ('idp', "International Driving Permit")

class LicenseIssuingAuthorityChoices(models.TextChoices):
    STATE_TRANSPORT_DEPARTMENT = ('state_transport_department', "State Transport Department")
    REGIONAL_TRANSPORT_OFFICE = ('regional_transport_office', "Regional Transport Office (RTO)")
    UT_TRANSPORT_DEPARTMENT = ('ut_transport_department', "Union Territory Transport Department")
    MINISTRY_OF_ROAD_TRANSPORT_AND_HIGHWAYS = ('morth', "Ministry of Road Transport and Highways (MoRTH)")

class RoleChoices(models.TextChoices):
    LEARNER = 'learner', 'Learner'
    INSTRUCTOR = 'instructor', 'Instructor'
    SCHOOL = 'school', 'School'

class PlanChoices:
    FREE = 'Free_pack'
    STARTER = 'Starter_pack'
    PRO = 'Pro_pack'
    ENTERPRISE = 'Enterprise_pack'