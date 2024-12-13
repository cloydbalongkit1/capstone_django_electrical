from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.core.serializers import serialize
from django.contrib import messages

from .models import User, Calculations, ContactUs
from .util_views import is_subscribe
# from electrical_calculations import settings

 

from datetime import datetime
from electricpy import visu, phasors
import matplotlib.pyplot as plt
import numpy as np
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
        
    return render(request, "circuits/login.html", {"title": "Login"})


@login_required
def user_logout(request):
    logout(request)
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
                "message": "Username is already taken! Try a different one.",
                "title": "Register"
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


def home(request):
    return render(request, "circuits/home.html", {"title": "Home"})


def about(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:
            ContactUs.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been successfully sent.")
            return HttpResponseRedirect(reverse('home'))
        else:
            error_message = "All fields are required. Please fill out every field."
            return render(request, "circuits/about.html", {"title": "About", "error_message": error_message})

    return render(request, "circuits/about.html", {"title": "About"})



@login_required
def query_messages(request):
    unread_count = ContactUs.objects.filter(is_read=False).count()
    return JsonResponse({"unread_count": unread_count})



@login_required
def contacted_messages(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    contact_us = ContactUs.objects.all().order_by("-created_at")
    return render(request, "circuits/contacted_mgs.html", {
            "title": "Contacted Messages",
            "contact_us": contact_us,
        })



@login_required
def contacted_message(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    content = get_object_or_404(ContactUs, id=id)
    return render(request, "circuits/contacted_mg.html", {
        "title": f"{content.id}/{content.name}",
        "content": content,
    })



@login_required
def calculate(request):
    has_subscription = is_subscribe(request.user)
    return render(request, "circuits/calculate.html", {"title": "Calculate", "has_subscription": has_subscription})


@login_required
def power_triangle(request):
    if request.method == "POST":
        try:
            has_subscription = is_subscribe(request.user)

            P = request.POST.get('power_triangle_P')
            Q = request.POST.get('power_triangle_Q')
            S = request.POST.get('power_triangle_S')
            pf = request.POST.get('power_triangle_pf')

            P = float(P) if P else None
            Q = float(Q) if Q else None
            S = float(S) if S else None
            pf = float(pf) if pf else None
            
            if sum(x is not None and x != 0 for x in [P, Q, S, pf]) < 2:
                return render(request, "circuits/calculate.html", {
                    "error": "Please provide at least two non-zero inputs.",
                    "title": "Error"
                })

            plt.figure()
            visu.powertriangle(P=P, Q=Q, S=S, PF=pf)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close()

            values = {
                "name": "power_triangle",
                "P":P, 
                "Q":Q, 
                "S":S, 
                "pf":pf
            }

            json_values = json.dumps(values)

            return render(request, "circuits/calculate.html", {
                    "plot_image": image_base64, # save the plot image database (todo!)
                    "display": True, 
                    "show_output": 'true', # used in JS
                    "values": json_values,
                    "title": "Calculate Result",
                    "power_triangle": "True",
                    "has_subscription": has_subscription
                })

        except ValueError:
            return render(request, "circuits/calculate.html", {
                "error": "Invalid input. Please ensure all values are numbers.",
                "title": "Error"
                })




@login_required
def save_calc(request):
    if request.method == "POST":
        try:
            datas = json.loads(request.body)
            name = datas.get("name")
            # imgBase64 = datas.get("imgBase64")
            data_body = datas.get("body")
            data_body.pop('csrfmiddlewaretoken', None)
            
            Calculations.objects.create(name=name, datas=json.dumps(datas), created_by=request.user)

            return JsonResponse({
                "status": "success",
                "message": "Calculation saved successfully."
            })

        except json.JSONDecodeError:
            return JsonResponse({
                    "status": "error",
                    "message": "Invalid JSON data received."
                }, status=400)
        
        except Exception as e:
            print("Error saving calculation:", str(e))
            return JsonResponse({
                "status": "error",
                "message": "An error occurred while saving the calculation."
            }, status=500)
        


@login_required
def user_calculations(request):
    calculations = Calculations.objects.filter(created_by=request.user).order_by("-created_at")
    serialized_data = serialize("json", calculations)
    parsed_calculations = json.loads(serialized_data)

    refined_data = []

    for obj in parsed_calculations:
        context = obj["fields"].get("name")

        if context == "power_triangle":
            refined_data.append(
                {
                    "id": obj["pk"],
                    "name": obj["fields"].get("name") or "Unknown",
                    "power_triangle_P": json.loads(obj["fields"]["datas"]).get("body", {}).get("power_triangle_P") or 0,
                    "power_triangle_Q": json.loads(obj["fields"]["datas"]).get("body", {}).get("power_triangle_Q") or 0,
                    "power_triangle_S": json.loads(obj["fields"]["datas"]).get("body", {}).get("power_triangle_S") or 0,
                    "power_triangle_pf": json.loads(obj["fields"]["datas"]).get("body", {}).get("power_triangle_pf") or 0,
                    "created_at": datetime.strptime(obj["fields"].get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y/%m/%d - %H:%M"),
                    "data_calculation_img": json.loads(obj["fields"]["datas"]).get("imgBase64") or 0,
                } 
            )

        if context == "phasor":
            refined_data.append(
                {
                    "id": obj["pk"],
                    "name": obj["fields"].get("name") or "Unknown",
                    "V1_magnitude": json.loads(obj["fields"]["datas"]).get("body", {}).get("V1_magnitude") or 0,
                    "V1_angle": json.loads(obj["fields"]["datas"]).get("body", {}).get("V1_angle") or 0,
                    "V2_magnitude": json.loads(obj["fields"]["datas"]).get("body", {}).get("V2_magnitude") or 0,
                    "V2_angle": json.loads(obj["fields"]["datas"]).get("body", {}).get("V2_angle") or 0,
                    "V3_magnitude": json.loads(obj["fields"]["datas"]).get("body", {}).get("V3_magnitude") or 0,
                    "V3_angle": json.loads(obj["fields"]["datas"]).get("body", {}).get("V3_angle") or 0,
                    "created_at": datetime.strptime(obj["fields"].get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y/%m/%d - %H:%M"),
                    "data_calculation_img": json.loads(obj["fields"]["datas"]).get("imgBase64") or 0,
                }
            )

    page = request.GET.get("page", 1)
    paginator = Paginator(refined_data, 3)  

    try:
        refined_data_page = paginator.page(page)
    except:
        refined_data_page = paginator.page(1) 

    return render(request, "circuits/home.html", {
            "title": "Previous Calculations", 
            "refined_data": refined_data_page, 
            "previous": True
        })



@login_required
def profile_view(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "circuits/profile.html", {
        "title": "Profile",
        "user": user
    })


@login_required
def edit_profile(request):
    if request.method == "POST":
        first_name = request.POST.get("First_Name", "").strip() or ""
        last_name = request.POST.get("Last_Name", "").strip() or ""
        bio = request.POST.get("Bio", "").strip() or ""
        work = request.POST.get("Work", "").strip() or ""
        location = request.POST.get("Location", "").strip() or ""

        user = get_object_or_404(User, id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.bio = bio
        user.work = work
        user.location = location
        user.save()

        return HttpResponseRedirect(reverse("profile_view"))

    return render(request, "circuits/update_profile.html", {
        "title": "Update Profile"
    })



@login_required
def phasor_diagram(request):
    if request.method == "POST":
        try:
            has_subscription = is_subscribe(request.user)

            V1_magnitude = float(request.POST.get("V1_magnitude", 0))
            V1_angle = float(request.POST.get("V1_angle", 0))
            V2_magnitude = float(request.POST.get("V2_magnitude", 0))
            V2_angle = float(request.POST.get("V2_angle", 0))
            V3_magnitude = float(request.POST.get("V3_magnitude", 0))
            V3_angle = float(request.POST.get("V3_angle", 0))

            if not any([V1_magnitude, V2_magnitude, V3_magnitude]):
                    return render(request, "circuits/calculate.html", {
                        "error": "Please provide at least one phasor magnitude.",
                        "title": "Error"
                    })

            values = {
                "name": "phasor_diagram",
                "V1_magnitude":V1_magnitude, 
                "V1_angle": V1_angle, 
                "V2_magnitude": V2_magnitude, 
                "V2_angle": V2_angle,
                "V3_magnitude": V3_magnitude,
                "V3_angle": V3_angle
            }

            json_values = json.dumps(values)

            voltages = np.array([
                [V1_magnitude, V1_angle],
                [V2_magnitude, V2_angle],
                [V3_magnitude, V3_angle],
            ])

            plt.figure()

            phasors_out = phasors.phasorlist(voltages)
            visu.phasorplot(phasors_out, colors=["red", "green", "blue"])

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            plot_image = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()

            plt.close()

            return render(request, "circuits/calculate.html", {
                "title": "Phasor Diagram",
                "display": True,
                "phasor_diagram": True,
                "show_output": 'true',
                "values": json_values,
                "plot_image": plot_image,
                "has_subscription": has_subscription
            })
        
        except ValueError:
            return render(request, "circuits/calculate.html", {
                "error": "Invalid input. Please ensure all values are numbers.",
                "title": "Error"
            })



@require_POST
@login_required
def delete_previous_calc(request, id):
    try:
        obj_prev = get_object_or_404(Calculations, id=id)
        obj_prev.delete()

        return JsonResponse({"message": "Deleted successfully!"}, status=200)
    
    except Calculations.DoesNotExist:
        return JsonResponse({"error": "Item not found!"}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    



@login_required
def help_solve(request):
    """
    This feature will be under development for future. (Dont have much time!)
    
    Feature: This is like a Stack-Overflow - application. 
    
    All electrical problems, forums will be raised.
    All users can comment, teach, recommend for the problem's solutions.

    """
    
    return render(request, "circuits/help.html", {"title": "Help Page"})



@login_required
def electrical_theory(request):
    """
    This feature will be all about electrical engineering theories and lectures that will help students.

    All users can view on this and study. 

    Markup language will be use for Input Data and save it to the backend DB.

    Planning to make another app on this or another API.

    """
    
    return render(request, "circuits/theory.html", {"title": "Electrical Theory"})