from django.contrib import admin
from users.models import User, Skills,\
    AddressDetails, Country, District, EducationDetails,\
    ExperienceDetails, Province, TrainingDetails, University,\
    Profile, SocialMedias

# Register your models here.
admin.site.register(User)
admin.site.register(Skills)
admin.site.register(AddressDetails)
admin.site.register(Country)
admin.site.register(District)
admin.site.register(EducationDetails)
admin.site.register(ExperienceDetails)
admin.site.register(Province)
admin.site.register(TrainingDetails)
admin.site.register(University)
admin.site.register(Profile)
admin.site.register(SocialMedias)

