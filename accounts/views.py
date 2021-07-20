from accounts.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.views.generic import (
    ListView, 
    CreateView,
)
from .forms import UserActivationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyWishListsView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'my_lists'
    template_name = 'wish/my_lists.html'

    def get_queryset(self):
        return CustomUser.objects.filter(responsible_by=self.request.user)

class RecWishListsView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'received_lists'
    template_name = 'wish/received_lists.html'

    def get_queryset(self):
        matched_responsibilities = CustomUser.objects.filter(responsible_by=self.request.user)
        return CustomUser.objects.filter(assigned_to__in=matched_responsibilities)

@login_required        
def complete_user_activation(request, user_id):
    current_user = CustomUser.objects.get(id=user_id)

    if user_id == request.user.id:
        if request.method == 'POST':
            form = UserActivationForm(request.POST)

            if form.is_valid():
                current_user.first_name = form.cleaned_data['first_name']
                current_user.last_name = form.cleaned_data['last_name']
                current_user.password = form.cleaned_data['password1']
                current_user.save()
                return redirect('home')

        else: 
            form = UserActivationForm()

        return render(request, 'registration/complete_activation.html', {'form': form})

    else:
        return HttpResponseForbidden() 