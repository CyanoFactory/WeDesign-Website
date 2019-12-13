"""
Copyright (c) 2019 Gabriel Kind
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

from django.shortcuts import redirect

from wedesign.helpers import render_queryset_to_response
from .forms import CreateProfileForm


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
