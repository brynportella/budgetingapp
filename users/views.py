# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('onboarding')
    template_name = 'signup.html'
    def form_valid(self, form):
        to_return = super().form_valid(form)
        login(self.request, self.object)
        return to_return

