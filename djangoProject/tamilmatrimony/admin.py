from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import profiles, ShownInterest
# Register your models here.



class ProfileModelAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ["tmId","__str__","image", "image2", "image3", "image4", 'timestamp', 'updated', 'week_number', 'no_of_contacts']
    list_display_links = ["__str__"]
    list_filter = ["gender","timestamp","dateOfBirth"]
    search_fields = ["name","countryOfOrigin","motherTongue"]


    class Meta:
        model = profiles

class ShownInterestAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ["pId", "intrestedPId"]

    class Meta:
        model = ShownInterest


admin.site.register(profiles, ProfileModelAdmin)
admin.site.register(ShownInterest, ShownInterestAdmin)
