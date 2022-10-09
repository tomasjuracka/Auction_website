# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.urls import reverse_lazy
from django.views import generic


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email", "username", "password1", "password2"
        )


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = 'accounts/signup.html'
