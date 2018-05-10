from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import *
from .forms import *


def index(request):
    return render(request, "openclass/home.html")

def workshops_list(request):
    w = Workshop.objects.all()
    return render(request, "openclass/listworkshop.html", {"list":w})

def workshops_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop,pk=workshop_id)
    return render(request, "openclass/workshop.html",{"workshop":workshop})

def members_list(request):
    return HttpResponse('members_list')

def members_detail(request, member_id):
    return HttpResponse('members_detail')

def badges_list(request):
    return HttpResponse('badges_list')

@login_required()
def profile(request):
    return render(request, "openclass/profile.html")

def prefs(request):
    user = request.user
    age = user.profile.get_age
    return render(request, "openclass/user-preferences.html", {"age":age})

def signup(request):

    tags = Tag.objects.all()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.score = 0
            profile.save()
            #should verify the user via email
            login(request, user)
            return redirect('/profile')

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context = {"user_form":user_form, "user_profile_form":user_profile_form}
    return render(request, 'openclass/signup.html', context)


def submit_workshop(request):
    if request.method == "POST":
        workshop_form = WorkshopForm(request.POST)
        if workshop_form.is_valid():
            workshop_form.save()
            return HttpResponse("Thanks, Your workshop has been submitted")

    else:
        workshop_form = WorkshopForm()

    context = {"workshop_form": workshop_form}
    return render(request, "openclass/submit_workshop.html", context)


def moderation(request):
    return render(request, "openclass/moderation.html")
