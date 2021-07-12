from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import CustomUser

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class MyWishListsView(ListView):
    model = CustomUser
    context_object_name = 'my_lists'
    template_name = 'my_lists.html'

    def get_queryset(self):
        return CustomUser.objects.filter(responsible_by=self.request.user)

class RecWishListsView(ListView):
    model = CustomUser
    context_object_name = 'received_lists'
    template_name = 'received_lists.html'

    def get_queryset(self):
        matched_responsibilities = CustomUser.objects.filter(responsible_by=self.request.user)
        return CustomUser.objects.filter(assigned_to__in=matched_responsibilities)
