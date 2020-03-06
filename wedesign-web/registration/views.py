"""
Copyright (c) 2019 Gabriel Kind
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from wedesign.helpers import render_queryset_to_response
from .forms import CreateProfileForm, ChangeProfileForm


def register(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)

        if form.is_valid():
            form.save(request)
            return redirect("wedesign:index")
    else:
        form = CreateProfileForm()

    return render_queryset_to_response(
        request,
        template="registration/register.html",
        data={"form": form}
    )


@login_required
def account_change(request):
    success = False
    if request.method == 'POST':
        form = ChangeProfileForm(request, request.POST)

        if form.is_valid():
            form.save()
            success = True
    else:
        form = ChangeProfileForm(request)

    return render_queryset_to_response(
        request,
        template="registration/account_change.html",
        data={"form": form, "success": success}
    )