from django.db import models
from django import forms
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import *
import string, random
from datetime import date
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator

def upload_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)


class profiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE,)
    #Basics & Lifestyle
    tmId = models.AutoField(primary_key=True)
    pId = models.CharField(max_length=10, default='TMG')
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)

    image = models.ImageField(upload_to= upload_location,null=True, blank=True,default="default/pimage.png")
    thumbnail = ImageSpecField(

        source='image', processors=[SmartResize(600,600)],format='JPEG',
        options={'quality':70},

    )
    image2 = models.ImageField(upload_to= upload_location,null=True, blank=True,default="default/pimage.png")
    thumbnail2 = ImageSpecField(

        source='image2', processors=[SmartResize(600,600)],format='JPEG',
        options={'quality':70},

    )
    image3 = models.ImageField(upload_to= upload_location,null=True, blank=True,default="/media/default/pimage.png")
    thumbnail3 = ImageSpecField(

        source='image2', processors=[SmartResize(600,600)],format='JPEG',
        options={'quality':70},

    )
    image4 = models.ImageField(upload_to= upload_location,null=True, blank=True,default="/media/default/pimage.png")
    thumbnail4 = ImageSpecField(

        source='image2', processors=[SmartResize(600,600)],format='JPEG',
        options={'quality':70},

    )
    maritalStatus_choices = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    )
    maritalStatus = models.CharField(max_length=25, choices=maritalStatus_choices, default='single')
    body_Type = models.CharField(max_length=15)
    height = models.CharField(max_length=15)
    weight = models.CharField(max_length=15)
    matrimonyProfileFor_choices = (
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('self', 'Self'),
    )
    matrimonyProfileFor = models.CharField(max_length=25, choices=matrimonyProfileFor_choices, default='personal')
    drink = models.CharField(max_length=15)
    smoke = models.CharField(max_length=15)
    dateOfBirth = models.DateTimeField('Date of Birth/Time - Format : YYYY-MM-DD HH:MM', auto_now=False, auto_now_add=False,)



    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    age = models.IntegerField(default=0)
    motherTongue = models.CharField(max_length=50)
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),

    )
    gender = models.CharField(max_length=15, choices=gender_choices)
    blood_group = models.CharField(max_length=20,default="not specified")
    diet = models.CharField(max_length=20)

    #Religious / Social & Astro Background

    #timeOfBirth = models.TimeField( default= "00:00")
    religion_choices = (
        ('hindu','Hindu'),
        ('cristian','Cristian'),
        ('muslim','Muslim'),
        ('sikh','Sikh'),
        ('buddhist','Buddhist')
    )
    religion = models.CharField(max_length=50, choices=religion_choices)
    caste = models.CharField(max_length=50)
    sub_caste = models.CharField(max_length=25)
    #DOB
    placeOfBirth = models.CharField(max_length=30)
    rassi = models.CharField(max_length=30)

    #Education & Career

    education = models.CharField(max_length=50)
    education_detail = models.CharField(max_length=50)
    occupation_detail = models.CharField(max_length=100)
    annual_income = models.CharField(max_length=20, default="not specified")
    current_location = models.CharField(max_length=25)

    #Family Details

    father_occupation = models.CharField(max_length=50)
    mobile_no = models.IntegerField(default=1234567890 , validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    mother_occupation = models.CharField(max_length=50)
    native_place = models.CharField(max_length=50, default="")
    native_city = models.CharField(max_length=50, default="")
    dist_choices=(
    'Beed', 'Latur'
    )

    native_dist = models.CharField(max_length=50, default="")
    no_of_sisters = models.IntegerField(default=0)
    no_of_brother = models.IntegerField(default=0)


    #no of contacts requested
    week_number = models.IntegerField(default=0)
    no_of_contacts = models.IntegerField(default=0)

    #partner preferences

    p_age_min = models.IntegerField(default=0)
    p_age_max = models.IntegerField(default=0)
    p_Marital_Status = models.CharField(max_length=10)
    p_Body_Type = models.CharField(max_length=25)
    p_Complexion = models.CharField(max_length=25)
    p_Height = models.CharField(max_length=25)

    p_Diet =  models.CharField(max_length=25)
    p_Manglik =  models.CharField(max_length=25)
    p_Religion =  models.CharField(max_length=25)
    p_Caste =  models.CharField(max_length=25)
    p_Mother_Tongue =  models.CharField(max_length=25)
    p_Education =  models.CharField(max_length=25)
    p_Country_Of_Residence =  models.CharField(max_length=25)
    p_State =  models.CharField(max_length=25)


    timestamp = models.DateTimeField(auto_now=False, auto_now_add= True)

    def __str__(self):
        return self.pId

    def get_absolute_url(self):
        return reverse("profiles:details", kwargs={"slug":self.slug})
    class Meta:
        ordering =["-timestamp","-updated"]

class ShownInterest(models.Model):
    pId = models.CharField(max_length=10, default='TMG')
    intrestedPId = models.CharField(max_length=10, default='TMG')


def create_slug(instance, new_slug=None):
    slug= slugify(instance.name)
    if new_slug is not None:
        slug= new_slug
    qs = profiles.objects.filter(slug=slug).order_by("-tmId")
    exists = qs.exists()
    if exists:
        new_slug= "%s-%s" %(slug, qs.first().tmId)
        return create_slug(instance, new_slug = new_slug)
    return slug


def pre_save_post_signal_reciever(sender, instance, *args, **kwargs):


    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_signal_reciever, sender=profiles)
