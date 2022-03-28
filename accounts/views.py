from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
@login_required(login_url='accounts:login')
def home(request):
    return render(request, 'accounts/index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        form = UserForm()

        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'account has been created for ' + user)
                return redirect('accounts:login')

        return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password1')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('accounts:home')
            else:
                messages.info(request, 'email or password is not valid')

        form = UserForm
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')

#
# def create(validated_data):
#     user = User(
#         username=validated_data['username']
#     )
#     user.set_password(validated_data['password'])
#     user.save()
#     return user
