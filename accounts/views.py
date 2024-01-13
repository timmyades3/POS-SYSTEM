from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .forms import Createuser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
class index(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "login"

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class Register(View):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            form = Createuser(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")

                # Authenticate and log in the user
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(
                        request,
                        f"Welcome {username} you have successfully created an account",
                    )
                    return redirect(reverse('start_fido2'))

                else:
                    messages.error(request, "Failed to log in. Please try again.")
                

            return render(request, "register.html", {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            form = Createuser()
        return render(request, "register.html", {"form": form})
    

def login_user_in(request, username):
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    if "next" in request.POST:
        return redirect(request.POST.get("next"))
    else:
        return redirect(reverse('accounts:index'))
    

class Login(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                from mfa.helpers import has_mfa
                res =  has_mfa(username = username,request=request) # has_mfa returns false or HttpResponseRedirect
                if res:
                    return res
                return login_user_in(request,username=user.username)     
            elif user is None:
                error_message = "User does not exist."
        return render(request, "login.html", {"error_message": error_message})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, "login.html")


class Logout(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "login"

    def get(self, request):
        logout(request)
        return render(request, "logout.html")


# Create your views here.
