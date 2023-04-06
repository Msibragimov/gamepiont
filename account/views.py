from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

from .forms import RegistrationForm, LoginUserForm
from .tasks import send_email_on_registration
from .utils import generate_token
from .models import Account


def login_request(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or 'homepage'
        return redirect(next_url)
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect("homepage")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = LoginUserForm()
    return render(request=request, template_name="accounts/login.html", context={"login_form":form})


def log_user_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            send_email_on_registration(current_site.domain, user.id)
            messages.success(request, "Check your email to activate your account" )
            return redirect('check_email')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request, 'accounts/register.html', context={'register_form': form, 'next': request.GET.get('next') or 'homepage'})


def check_email(request):
    return render(request, 'accounts/check_email.html')


def activate_user(request, uid, token):
    user = Account.objects.filter(id=uid).first()
    if user:
        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('homepage'))
    return HttpResponse(content='Invalid activation link', status=401)


def homepage(request):
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'accounts/index.html')