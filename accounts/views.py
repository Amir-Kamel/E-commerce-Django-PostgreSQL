from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import UserRegistrationForm



class SignupView(CreateView):
    form_class = UserRegistrationForm
    form_title='User Registration'
    template_name = "registration/login.html"
    extra_context = {
        "form_title": "Sign up"
    }
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response

class CustomLoginView(LoginView):
    form_title="Login"
    template_name = 'registration/signup.html'
    redirect_authenticated_user = True
    extra_context = {"form_title": "Login"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Login"
        return context


@login_required
def logout_view(request):
    logout(request)
    return redirect('all_products')