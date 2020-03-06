"""
Copyright (c) 2019 Gabriel Kind
Hochschule Mittweida, University of Applied Sciences

Released under the MIT license
"""

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from wedesign.layout import Panel


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Username or Mail"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Panel(
                'Login',
                'username',
                'password',
            ),
            FormActions(
                Submit('submit', 'Login')
            )
        )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            if "@" in username:
                try:
                    u = get_user_model().objects.get(email=username)
                    username = u.username
                except ObjectDoesNotExist:
                    pass

            self.user_cache = authenticate(username=username,
                                            password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CreateProfileForm(forms.Form):
    username = forms.SlugField(
        required=True,
        widget=forms.TextInput,
        label="Username",
        max_length=20
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput,
        label="E-Mail address",
        max_length=254,
        help_text="For password recovery. The mail address is not validated"
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        max_length=254
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        max_length=254
    )

    captcha = forms.CharField(
        label="Challenge",
        widget=forms.TextInput,
        required=True,
        help_text="Type the reverse complement of ATCGAAGG"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Panel(
                'Account information',
                'username',
                'email',
                'password',
                'password2'
            ),
            Panel(
                'Challenge',
                'captcha'
            ),
            FormActions(
                Submit('submit', 'Register')
            )
        )

    def clean(self):
        username = self.cleaned_data.get("username")
        if username:
            if get_user_model().objects.filter(username=username).exists():
                raise forms.ValidationError(
                    "Username already in use",
                    params={'username': "Username"})

        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2:
            if password != password2:
                raise forms.ValidationError(
                    "The passwords mismatch",
                    params={'password': "Password"})

        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email and email2:
            if email != email2:
                raise forms.ValidationError(
                    "The mail addresses mismatch",
                    params={'email': "email"})

            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "E-Mail address already in use",
                    params={'email': "email"})

        captcha = self.cleaned_data.get("captcha")

        if captcha:
            if captcha.strip().lower() != "ccttcgat":
                raise forms.ValidationError(
                    "You failed in biology :(",
                    params={'captcha': "captcha"})

        return self.cleaned_data

    def save(self, request):
        user = get_user_model().objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )

        if self.cleaned_data.get("first_name"):
            user.first_name = self.cleaned_data["first_name"]

        if self.cleaned_data.get("last_name"):
            user.last_name = self.cleaned_data["last_name"]

        if self.cleaned_data.get("affiliation"):
            user.profile.affiliation = self.cleaned_data["affiliation"]
            user.profile.save()

        user.save()

        login_user = authenticate(username=user.username, password=self.cleaned_data["password"])
        login(request, login_user)


class ChangeProfileForm(forms.Form):
    username = forms.SlugField(
        required=True,
        widget=forms.TextInput,
        label="Username",
        max_length=20
    )

    first_name = forms.CharField(
        widget=forms.TextInput,
        required=False,
        label="First name",
        max_length=254
    )

    last_name = forms.CharField(
        widget=forms.TextInput,
        required=False,
        label="Last name",
        max_length=254
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput,
        label="E-Mail address",
        max_length=254
    )

    password = forms.CharField(
        label="Your Password",
        widget=forms.PasswordInput,
        help_text="Enter your current password to verify your changes",
        max_length=254
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Panel(
                'Account information',
                'username',
                'first_name',
                'last_name',
                'email',
                'password'
            ),
            FormActions(
                Submit('submit', 'Save changes')
            )
        )

        self.request = request
        user = self.request.user

        self.fields["username"].initial = user.username
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email

    def clean(self):
        password = self.cleaned_data.get('password')

        if password:
            auth = authenticate(username=self.request.user.username,
                                password=password)

            if auth is None:
                raise forms.ValidationError(
                    "Wrong password",
                    code='invalid_login',
                    params={'password': self.fields["password"].label},
                )

        username = self.cleaned_data.get('username')

        if username:
            if username != self.request.user.username:
                if User.objects.filter(username=username).exists():
                    raise forms.ValidationError(
                        "Username already in use",
                        params={'username': "username"})

        email = self.cleaned_data.get("email")
        if email:
            if email != self.request.user.email:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError(
                        "E-Mail address already in use",
                        params={'email': "email"})

        return self.cleaned_data

    def save(self):
        u = self.request.user

        u.username = self.cleaned_data.get('username')
        u.email = self.cleaned_data.get('email')
        u.first_name = self.cleaned_data.get('first_name')
        u.last_name = self.cleaned_data.get('last_name')
        u.save()
