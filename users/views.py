from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Intern
from .forms import CustomUserCreationForm, ProfileForm, InternForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.template.defaulttags import register
from .utils import createAccounts
import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from openpyxl import Workbook


def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="credits.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Students-Credits"

    # Add headers
    headers = ["Name", "Regno", "Intern-1", "Intern-2", "Intern-3", "Intern-4", "Credits"]
    ws.append(headers)

    # Add data from the model
    products = Profile.objects.exclude(user__is_superuser=True)
    for product in products:
        interns = product.intern_set.filter(accepted=True)
        listItem = [str(product.name), str(product.regno)]
        for intern in interns:
            listItem.append(int(intern.creditsrewarded))
        c = interns.count()
        if c < 4:
            t = c
            while t<4:
                listItem.append(0)
                t = t + 1

        listItem.append(int(product.creditsearned))
        ws.append(listItem)

    # Save the workbook to the HttpResponse

    wb.save(response)
    return response



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def logoutUser(request):
    logout(request)
    messages.info(request, "User successfully logged out")
    return redirect('login')


def loginUser(request):
    
    
    if request.method == 'POST':
        username=request.POST['username']
        password = request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, "User successfully logged in")

            return redirect('account')
        else:
            messages.error(request, "Credentials wrong")

    return render(request, 'users/login_register.html')






@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    interns = profile.intern_set.all()

    isAccepted = profile.intern_set.filter(accepted=True).exists()
    isNotReviewed = profile.intern_set.filter(reviewed=False).exists()
    isRejected = profile.intern_set.filter(reviewed=True, accepted=False).exists()

    context = {'profile':profile, 'interns': interns, 'isAccepted': isAccepted, 'isNotReviewed': isNotReviewed, 'isRejected': isRejected}
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url="login")
def applyIntern(request):
    profile = request.user.profile
    form = InternForm()

    
    if request.method == 'POST':
        form = InternForm(request.POST, request.FILES)
        if form.is_valid():
            intern = form.save(commit=False)
            intern.owner = profile
            intern.save()

            messages.success(request,'Intern was applied successfully')
            return redirect('apply')

        else:
            messages.error(request, 'Submit proper files!')
    


    context = {'form':form}
    return render(request, 'users/apply.html', context)


def is_superuser(user):
    return user.is_superuser



@user_passes_test(is_superuser, login_url=reverse_lazy('login'))
def acceptIntern(request, intern_id):
    intern = Intern.objects.get(pk=intern_id)
    intern.reviewed = True
    intern.accepted = True

    credit = 0
    if request.method == "POST":
        credit = int(request.POST.get('credit_input', 0))
        
        intern.creditsrewarded = credit
        intern.owner.creditsearned += credit
        intern.owner.save()  
        intern.save()
        messages.success(request, 'Intern accepted successfully')
        return redirect('review')
    context = {'page': 'accept'}

    return render(request, 'users/review.html', context)


    

@user_passes_test(is_superuser, login_url=reverse_lazy('login'))
def reviewInterns(request):
    interns = Intern.objects.filter(reviewed=False)
    for_review = interns.count()
    context = {'interns': interns, 'for_review': for_review}
    return render(request, 'users/review.html', context)


def rejectIntern(request, intern_id):
    intern = Intern.objects.get(pk=intern_id)
    intern.reviewed = True
    intern.accepted = False
    intern.save()
    messages.success(request, 'Intern rejected successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(is_superuser, login_url=reverse_lazy('login'))
def displayInterns(request):
    profiles = Profile.objects.exclude(user__is_superuser=True)

    filtered_interns = {}

    for profile in profiles:
        filtered_interns[profile.id] = profile.intern_set.filter(~Q(reviewed=True) | ~Q(accepted=False))
    context = {'profiles': profiles, 'filtered_interns': filtered_interns}

    return render(request, 'users/interns.html', context)


@user_passes_test(is_superuser, login_url=reverse_lazy('login'))
def singleUserPage(request, id):
    profile = Profile.objects.get(pk=id)
    interns = profile.intern_set.all()

    isAccepted = profile.intern_set.filter(accepted=True).exists()
    isNotReviewed = profile.intern_set.filter(reviewed=False).exists()
    isRejected = profile.intern_set.filter(reviewed=True, accepted=False).exists()

    context = {'profile':profile, 'interns': interns, 'isAccepted': isAccepted, 'isNotReviewed': isNotReviewed, 'isRejected': isRejected}
    return render(request, 'users/user-profile.html', context)


@user_passes_test(is_superuser, login_url=reverse_lazy('login'))
def createUsers(request):
    if request.method == "POST":
        excel_file = request.FILES.get('excel_file')

        if excel_file:
            try:
                # Read the uploaded file using Pandas
                df = pd.read_excel(excel_file)
                
                # Call the function from utils.py to process the DataFrame
                createAccounts(df)

                return redirect('interns')  # Redirect to a success page or do something else on success
            except Exception as e:
                # Handle exceptions or display an error message
                error_message = f"Error processing file: {str(e)}"
                return redirect(request, 'create-users.html', {'error_message': error_message})

    return render(request, 'users/create-users.html')





