from django.views import generic
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from .forms import SignUpForm


class UserRegistrationView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

