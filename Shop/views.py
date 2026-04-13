from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Contact


# HOME
def index(request):
    return render(request, 'index.html')


# ABOUT
def about(request):
    return render(request, 'about.html')


# CONTACT
def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            msg=request.POST.get("msg")
        )
        return redirect('/contact/')

    data = Contact.objects.all()
    return render(request, 'contact.html', {"data": data})


# PRODUCTS (PROTECTED)
def products(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    return render(request, 'product.html')


# LOGIN VIEW (FIXED + SAFE)
def loginview(request):
    if request.user.is_authenticated:
        return redirect('/home/')   # prevents re-login

    if request.method == "POST":
        username = request.POST.get("userName")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# SIGNUP VIEW (CLEAN + SAFE)
def signupview(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        username = request.POST.get("userName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        # Password match check
        if password != cpassword:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        # Username check
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = firstName
        user.last_name = lastName
        user.save()

        return redirect('/login/')

    return render(request, 'signup.html')


# LOGOUT (FIXED)
def logoutview(request):
    logout(request)
    return redirect('/home/')