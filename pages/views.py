from accounts.models import CustomUser
from groups.models import CustomGroup, Assignments
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            current_user = self.request.user
            current_groups = CustomGroup.objects.filter(user=current_user).filter(closed=False)
            responsible_users = CustomUser.objects.filter(responsible_by=current_user)
            current_closed_groups = CustomGroup.objects.filter(user=current_user).filter(closed='True')
            current_assignments = Assignments.objects.filter(group__in=current_closed_groups).order_by('-time')
            number_of_assignments = sum([
                len([assignment for assignment in assignments.assignments.filter(assignment__in=responsible_users)])
                    for assignments in current_assignments
                ])

            data['screen_name'] = get_name_or_email(current_user)
            data['current_user'] = current_user
            data['current_groups'] = current_groups
            data['number_of_assignments'] = number_of_assignments
        return data


def get_name_or_email(user):
        if user.first_name:
            return user.first_name
        else:
            return user.email

def get_possessive_ending(word):
        return word + "'" if word[-1] == 's' else word + "'s"