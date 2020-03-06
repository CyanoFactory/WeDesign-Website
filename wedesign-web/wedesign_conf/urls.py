"""
Copyright (c) 2019 Gabriel Kind <gkind@hs-mittweida.de>
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

import registration.views
from registration.forms import LoginForm

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('accounts/register/', registration.views.register, name="register"),
    path('accounts/edit/', registration.views.account_change, name="account_change"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('', include('wedesign.urls'))
]
