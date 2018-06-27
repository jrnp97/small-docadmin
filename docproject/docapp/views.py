from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
# from django.contrib.auth.views import LoginView

# Create your views here.


def index(request):
    return render(request, 'docapp/index.html')


def login(request):
    if request.method == 'POST':
        return redirect('docapp:index')
    else:
        return render(request, 'docapp/login.html')


# class Login(LoginView):
#     template_name = 'docapp/login.html'
#     success_url = reverse_lazy('docapp:index')

