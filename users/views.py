from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index:dashboard')
    form = LoginForm(request.POST or None)

    msg = None
    if request.method == "POST":

        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('index:dashboard')
            else:
                form.add_error('email', 'Email or Password is not correct')

    return render(request, "user/login.html", {"form": form})





