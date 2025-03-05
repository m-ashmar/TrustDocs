from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import logout

from rest_framework_simplejwt.views import TokenObtainPairView

# Web UI Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.user_type == 'institution':
                return redirect('download-document')
            return redirect('upload-document')  # Redirect after login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')  # Redirect to login after registration
        return render(request, 'users/register.html', {'errors': serializer.errors})
    return render(request, 'users/register.html')

# Keep your existing API views
def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login') 