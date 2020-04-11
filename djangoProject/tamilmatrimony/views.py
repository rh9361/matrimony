from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
#from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import profiles, ShownInterest
from .forms import Profileregister,Profileupdate


#email related imports
from django.core.mail import send_mail
from django.conf import settings

#no_of profiles contacted imports
from datetime import *

#write a generic function to get all basic information about logged in user
def getMemberInfo(username):
    print("inside getMemberInfo username : ", username)
    userRec=User.objects.all().filter(username=username)[0]
    isCordinator=userRec.groups.filter(name='cordinator').exists()
    isMemberMale=userRec.groups.filter(name='MemberMale').exists()
    isMemberFemale=userRec.groups.filter(name='MemberFemale').exists()

    # if queryset:
    #     isProfileCreated=True
    userInfo={'isCordinator':isCordinator, 'isMemberMale':isMemberMale,'isMemberFemale':isMemberFemale}
    print(userInfo)
    return userInfo;


def register(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        messages.error(request, "Please logout and try again!")
        return HttpResponseRedirect('/profiles/myprofile')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                messages.add_message(request,messages.SUCCESS,"Successfully created an User!")
                return HttpResponseRedirect("/profiles/")
        else:
            form = UserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })





def login_user(request):
    if request.user.is_authenticated:
        messages.add_message(request,messages.SUCCESS,"You are already logged in!")
        return HttpResponseRedirect("/profiles/")
    username = password = ''
    context = RequestContext(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print("TRying to login")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print("Login done")
                login(request, user)
                messages.add_message(request,messages.SUCCESS,"Logged in successfully!")
                return HttpResponseRedirect('/profiles/')
            else: return HttpResponse("You're account is disabled.")
        else:
            print("unknown user")
            messages.error(request,"username or Password invalid. Please try again!")
            return render_to_response(request, 'login.html', {}, context.flatten())
        print("POST method")
    print("default login page")
    return render(request, 'login.html', context=context.flatten())


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("/profiles/")

def profile_list(request):
    username=request.user.username
    isProfileCreated=False
    profile_gen=""
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        if isProfileCreated:
            profile_gen = profiles.objects.all().filter(user=userid).values('gender')[0]['gender']
            print('profile_gen:', type(profile_gen))
            print('profile_gen:', profile_gen)
        print('isProfileCreated:', isProfileCreated)
        if profile_gen:
            queryset = profiles.objects.all().exclude(gender=profile_gen).order_by('-timestamp')[:10]
        else:
            queryset = profiles.objects.all().order_by('-timestamp')[:10]
    else:
        queryset = profiles.objects.all().order_by('-timestamp')[:10]

    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    content = {
        "objectset": queryset,
        "title": "Home",
        'isProfileCreated': isProfileCreated
    }
    return render(request,"index.html", content)
    #return HttpResponse("<h1>Hello World</h1>")

def aboutUs(request):
    content = {
        "title": "AboutUs",
    }
    return render(request,"aboutUs.html", content)

def shownInterest(request):
    username=request.user.username
    isProfileCreated=False
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        print('isProfileCreated:', isProfileCreated)
        print('userid:', username)
        print('isProfileCreated:', isProfileCreated)
        qset=ShownInterest.objects.all().filter(pId='TMG0012').values('intrestedPId')
        list_qset=list(qset)
        list_intrestedPId=[]
        print('list_qset', type(list_qset))
        for i in range(len(list_qset)):
            print(list_qset[i]['intrestedPId'])
            list_intrestedPId.append(list_qset[i]['intrestedPId'])

        print('list_intrestedPId',list_intrestedPId)
        #queryset=ShownInterest.objects.all().filter(pId__in=['TMG0021','TMG0022'])
        print("asd",type(list_qset))
    queryset = profiles.objects.all().filter(pId__in=list_intrestedPId).order_by('-timestamp')
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)
    content = {
        "objectset": queryset1,
        "title": "ShownInterest"
    }

    return render(request,"shownInterest.html", content)

def profile_list_all(request):
    username=request.user.username
    isProfileCreated=False
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        if isProfileCreated:
            profile_gen = profiles.objects.all().filter(user=userid).values('gender')[0]['gender']
            print('profile_gen:', type(profile_gen))
            print('profile_gen:', profile_gen)
        print('isProfileCreated:', isProfileCreated)
        if profile_gen:
            queryset = profiles.objects.all().exclude(gender=profile_gen).order_by('-timestamp')
        else:
            queryset = profiles.objects.all().order_by('-timestamp')
    else:
        queryset = profiles.objects.all().order_by('-timestamp')

    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)
    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request,"profiles.html", content)

def thankyou(request):
    print("asdddddd - ",request.GET.get('pid'))

    username=request.user.username
    isProfileCreated=False
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        print('isProfileCreated:', isProfileCreated)
        print('isProfileCreated:', isProfileCreated)

    #increse count of profiles contacted
    week_number=str(datetime.today().isocalendar()[0])+ str(datetime.today().isocalendar()[1])
    print(week_number)

    #add row in shownInterest table
    intrestedPId = 'TMG00'+str(userid)
    #shownInterest_row = shownInterest(intrestedPId)
    #print("instance.pId - - - ", instance.pId)

    #send mail
    return render(request, "thankyou.html")

    #Rajkumar


def profile_search_list(request):
    print("Inside profile_search_list...!!")
    username=request.user.username
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        if isProfileCreated:
            profile_gen = profiles.objects.all().filter(user=userid).values('gender')[0]['gender']
            print('profile_gen:', type(profile_gen))
            print('profile_gen:', profile_gen)
        print('isProfileCreated:', isProfileCreated)
        if profile_gen:
            queryset = profiles.objects.all().exclude(gender=profile_gen).order_by('-timestamp')
        else:
            queryset = profiles.objects.all().order_by('-timestamp')
    else:
        queryset = profiles.objects.all().order_by('-timestamp')


    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query1 = request.GET.get('religion')
    query2 = request.GET.get('gender')
    query3 = request.GET.get('maritalstatus')
    query4 = request.GET.get('min_age')
    query5 = request.GET.get('max_age')

    if query1 :#and query2 and query3 and query4 and query5 :
        queryset = queryset.filter(religion__icontains=query1)#.filter( p_age_max__lte=query5)
        queryset = queryset.filter(age__gte=int(query4))
        queryset = queryset.filter(age__lte=int(query5))
        queryset = queryset.filter(gender=query2)
        queryset = queryset.filter(maritalStatus__icontains=query3)

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "page_list": queryset1,
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "profile_search.html", content)
    #return HttpResponse("<h1>Hello World</h1>")





def profile_search_id(request):
    print("Inside profile_search_list...!!")
    username=request.user.username
    if username:
        userInfo=getMemberInfo(username)
        userid = int(request.user.id)
        isProfileCreated = profiles.objects.filter(user=userid).exists()
        if isProfileCreated:
            profile_gen = profiles.objects.all().filter(user=userid).values('gender')[0]['gender']
            print('profile_gen:', type(profile_gen))
            print('profile_gen:', profile_gen)
        print('isProfileCreated:', isProfileCreated)
        if profile_gen:
            queryset = profiles.objects.all().exclude(gender=profile_gen).order_by('-timestamp')
        else:
            queryset = profiles.objects.all().order_by('-timestamp')
    else:
        queryset = profiles.objects.all().order_by('-timestamp')

    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query = request.GET.get('pid')

    if query:
        instance = get_object_or_404(profiles,pId=str(query))
        return HttpResponseRedirect(instance.get_absolute_url())

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "profile_search_id.html", content)
    #return HttpResponse("<h1>Hello World</h1>")



@login_required(login_url="/login/")
def profile_create(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        userid = int(request.user.id)
        queryset = profiles.objects.filter(user=userid)

        if queryset:
            messages.error(request, "You have already created a profile!")
            return HttpResponseRedirect('/profiles/myprofile/')

        form = Profileregister(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            if instance.pId == "TMG":
                instance.pId = "TMG" + "00" + str(instance.tmId)
                instance.save()
            messages.add_message(request,messages.SUCCESS,"Successfully created a profile!")
            return HttpResponseRedirect("/profiles/myprofile")
        else:
            form = Profileregister(request.POST or None, request.FILES or None)
    content = {
        "form": form,
        "title": "Create/Register"
    }

    return render(request, "register.html", content)


def profile_detail(request, slug=None):
    instance = get_object_or_404(profiles, slug=slug)
    print("request.method", request.method)
    no_of_contacts=profiles.objects.filter(user = request.user).values('no_of_contacts')[0]['no_of_contacts']
    if request.method=="POST":
        print("Inside post method")
        print(instance.pId)
        print(profiles.objects.filter(user = request.user).values('pId')[0]['pId'])
        var_pId=instance.pId
        var_intrestedPId=profiles.objects.filter(user = request.user).values('pId')[0]['pId']
        #insert record in ShownInterest
        rec_exists = ShownInterest.objects.filter(pId=var_pId).filter(intrestedPId=var_intrestedPId).exists()
        print('rec_exists', rec_exists)
        #insert record to ShownInterest only if not present else show diff message
        if not rec_exists:
            ShownInterest_rec = ShownInterest(pId=var_pId, intrestedPId=var_intrestedPId)
            ShownInterest_rec.save()
        week_number_tab=str(profiles.objects.filter(user = request.user).values('week_number')[0]['week_number'])
        week_number=str(datetime.today().isocalendar()[0])+ str(datetime.today().isocalendar()[1])
        print(week_number)
        print(week_number_tab)
        profiles_rec=profiles.objects.get(user = request.user)
        print('profiles_rec:', type(profiles_rec))
        if week_number == week_number_tab:
            print("Week number is same today and in table")
            print("So now increase counter")
            no_of_contacts=profiles.objects.filter(user = request.user).values('no_of_contacts')[0]['no_of_contacts']
            no_of_contacts=no_of_contacts+1
        else:
            no_of_contacts=1
            print("Chnage weeknumber and set counter to 1")
        profiles_rec.week_number=str(week_number)
        profiles_rec.no_of_contacts=str(no_of_contacts)
        print("no_of_contacts:", no_of_contacts)
        profiles_rec.save()
        print("record saved...!")

        #before sending mail check shownInterest table and its count it should be 3 or less then only send mail to both candidate
        #sendmail


        #send biodata-image and pics from DB
        #get images of candidate and bio-data
        print(instance.pId)
        his_her_mail_id=User.objects.filter(username=instance.user).values('email')[0]['email']
        his_her_id=instance.pId
        his_her_url=request.build_absolute_uri(instance.get_absolute_url())
        his_her_name=instance.name
        his_her_mobile_no=instance.mobile_no
        his_her_father_occupation=instance.father_occupation
        his_her_native_place=instance.native_place
        his_her_native_dist=instance.native_dist

        my_mail_id=User.objects.filter(username=request.user).values('email')[0]['email']
        my_id=profiles_rec.pId
        my_url=request.build_absolute_uri(profiles_rec.get_absolute_url())

        print("his_her_mail_id:",his_her_mail_id," ,  his_her_id:", his_her_id, "his_her_url:", his_her_url)
        print("my_mail_id:",my_mail_id,"  ,  my_id : ", my_id)

        if no_of_contacts<50:
            subject = 'Candidate with id '+str(my_id)+' is interested in your profile'
            print("to mail id : ", User.objects.filter(username=instance.user))
            message = 'Congratulations candidate with id '+str(my_id)+' is interested in your profile. Please click on below link to access his/her profile -\n{}'.format(my_url)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [his_her_mail_id,]
            send_mail(subject, message, email_from, recipient_list)

            subject = 'Thanks for showing interest in one of our candidate '+str(his_her_id)
            print("to mail id : ", User.objects.filter(username=instance.user))
            message = 'Thanks for showing interest in one of our candidate {}, if he/she is also find it interested then they will send notification.\n\
Still you can contact, more information -\n\
Parents occupation - {}\n\
Contact no - {}\n\
Native City - {}\n\
Dist - {}\n\
Please click on below link to access his/her profile -\n{}'.format(his_her_id, his_her_father_occupation, his_her_mobile_no, his_her_native_place, his_her_native_dist, his_her_url)
            print(message)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [my_mail_id,]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, "thankyou.html")


    def create_pid():
        if instance.pId == "TMG":
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()
    no_of_contacts=profiles.objects.filter(user = request.user).values('no_of_contacts')[0]['no_of_contacts']
    content = {
        "detail_object": instance,
        "title": "Detail",
        "no_of_profiles_contacted": no_of_contacts,

    }
    return render(request, "view_profile.html", content)

@login_required(login_url='/login/')
def my_profile(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        username = request.user.id
        instance1 = profiles.objects.filter(user = int(username))#get_object_or_404(profiles, user = int(username))
        if not instance1:
            messages.add_message(request,messages.ERROR,"Please create an Profile!")
            return HttpResponseRedirect("/profiles/create/")
        instance = get_object_or_404(profiles, user = int(username))

    else:
        messages.error(request, "Please login to view your profile!")
        return render_to_response('login.html', {}, context.flatten())

    def create_pid():
        if instance.pId == "TMG" :
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()

    # print("user.username : ", user.username)
    # print(type(user.username))
    content = {
        "detail_object": instance,
        "title": "my_Detail",
    }
    print("detail_object.user : ", content["detail_object"].user)
    print(type(content["detail_object"].user))

    return render(request, "view_profile.html", content)


@login_required(login_url="/login/")
def myprofile_update(request):
    context = RequestContext(request)
    if request.user.is_authenticated:
        username = request.user.id
        instance = get_object_or_404(profiles, user=int(username))
        form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()
            messages.add_message(request,messages.SUCCESS,"Successfully updated your profile!")
            return HttpResponseRedirect("/profiles/myprofile/")
        else:
            form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    else:
        messages.add_message(request,messages.ERROR,"Please login to edit your profile!")
        return HttpResponseRedirect("/login/")

    content = {
        "detail_object": instance,
        "title": "My Update Profile",
        "form":form,
    }
    return render(request, "profileupdate.html", content)


def profile_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "successfully updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Not updated!")

    content = {
        "detail_object": instance,
        "title": "Update Profile",
        "form":form,
    }
    return render(request, "profileupdate.html", content)



def profile_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    instance.delete()
    messages.success(request, "succesfully Deleted!")
    return redirect("profiles:list")
