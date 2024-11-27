from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import JsonResponse
from .models import User, Circuits

import electricpy as ep
from electricpy import fault, visu
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
import json

matplotlib.use('Agg')

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "circuits/login.html", {
                "message": "Invalid username and/or password!"
            })
        
    return render(request, "circuits/login.html")


def user_logout(requests):
    logout(requests)
    return HttpResponseRedirect(reverse("user_login"))



def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if password != confirm_password:
            return render(request, "circuits/register.html", {
                "message": "Passwords didn't match. Try again."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "circuits/register.html", {
                "message": "Username is already taken! Try a different one."
            })
        if User.objects.filter(email=email).exists():
            return render(request, "circuits/register.html", {
                "message": "Email is already registered! Use a different email."
            })

        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            return HttpResponseRedirect(reverse('user_login'))  
        except IntegrityError:
            return render(request, "circuits/register.html", {
                "message": "An error occurred while creating the account. Please try again."
            })
        
    return render(request, "circuits/register.html")


def home(requests):
    user = requests.user
    return render(requests, "circuits/home.html", {"user": str(user).title()})


def calculate(requests):
    return render(requests, "circuits/calculate.html")


def power_triangle(request):
    if request.method == "POST":
        try:
            P = request.POST.get('power_triangle_P')
            Q = request.POST.get('power_triangle_Q')
            S = request.POST.get('power_triangle_S')
            pf = request.POST.get('power_triangle_pf')

            P = float(P) if P else None
            Q = float(Q) if Q else None
            S = float(S) if S else None
            pf = float(pf) if pf else None

            if sum(x is not None for x in [P, Q, S, pf]) < 2:
                return render(request, "circuits/calculate.html", {"error": "Please provide at least two inputs."})

            visu.powertriangle(P=P, Q=Q, S=S, PF=pf)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

            values = {"P":P, "Q":Q, "S":S, "pf":pf}
            json_values = json.dumps(values)

            return render(request, "circuits/calculate.html", {
                    "plot_image": image_base64, 
                    "display": True, 
                    "show_output": 'true', # used in JS
                    "values": json_values
                })

        except ValueError:
            return render(request, "circuits/calculate.html", {"error": "Invalid input. Please ensure all values are numbers."})

    return render(request, "circuits/calculate.html", {"display": False})