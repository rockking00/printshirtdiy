from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login as user_login
from django.utils.http import url_has_allowed_host_and_scheme
from goods.models import Category


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user_login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    categories = Category.objects.all()
    content = {
        'categories': categories,
        'form': form,
        'user': request.user
    }
    return render(request, 'accounts/signup.html', content)


def login_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_login(request, user)
                return redirect(form.request.GET.get('next','/'))
            else:
                form.add_error(None, 'Incorrect username or password')
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form, 'categories': categories})
