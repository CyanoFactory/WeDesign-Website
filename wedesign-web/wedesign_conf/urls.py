"""
Copyright (c) 2019 Gabriel Kind <gkind@hs-mittweida.de>
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

from django.contrib import admin
from django.urls import path, include

import registration.views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', registration.views.register, name="register"),

    path('admin/', admin.site.urls),

    path('design/', include('wedesign.urls'))
]
