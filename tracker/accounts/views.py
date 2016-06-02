from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from .models import *
from .forms import *

"""
Patient registration page (index).
"""
def PatientReg(request):
    form = PatientRegForm(data=request.POST or None)
    
    user = request.user

    if not user.is_anonymous():
        return HttpResponseRedirect(reverse('login:login'))

    if form.is_valid():
        fName = form.cleaned_data.get('fName')
        lName = form.cleaned_data.get('lName')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        patient = Patient.objects.createPatient(fName, lName, email, password)
        patient.user.first_name = fName
        patient.user.last_name = lName
        patient.user.save()
        patient.save()

        user = authenticate(username=patient.email, password=password)
        login(request, user)

        logger.info("New User: First Name: " + str(fName) + " Last Name: " + str(lName) + " Email: " + str(email))

        return HttpResponseRedirect(reverse('registration:edit'))
    
    return render(request, 'registration/index.html', {'form': form})


"""
View that shows patient profile.
It is built from a form, but the form is not editable.
"""
@login_required
def PatientProfileView(request, key=None):
    user = request.user
    
    if not user.is_authenticated():
        return HttpResponseRedirect(reverse('login:login'))
    
    form = PatientProfileForm(data=request.POST or None, initial={
        'fName': patient.username,
        'lName': patient.lName,
        'email': patient.email,
    })

    return render(request, 'registration/profile.html', {
        'form': form,
        'patient': patient,
        'isPatient': isPatient,
        'nurseAdmit': nurseAdmit,
        'isAdmin': isAdmin,
        'docCanTransfer': docCanTransfer,
        'doctor': isDoctor,
        'prescription_list': prescription_list,
        'result_list': result_list,
    })