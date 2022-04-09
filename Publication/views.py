from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from Publication.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from Publication.forms import UserRegistrationForm
from Publication.models import Linkedin_Account, Linkedin_Profile_Info

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/signup.html", {"form": form})

@login_required
def mon_compte(request):
    current_user = request.user.email

    compte = Linkedin_Account.objects.get(linkedin_account=current_user)
    mss_sent = len(Linkedin_Profile_Info.objects.filter(associated_account=compte, message_sent=True))
    reponse = len(Linkedin_Profile_Info.objects.filter(associated_account=compte, replied=True))
    return render(request, "compte.html", context={"mss_sent": mss_sent, "reponse": reponse})