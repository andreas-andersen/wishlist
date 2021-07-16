from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            data['screen_name'] = get_name_or_username(self.request.user)
        return data


def get_name_or_username(user):
        if user.first_name:
            return user.first_name
        else:
            return user.username

def get_possessive_ending(word):
        return word + "'" if word[-1] == 's' else word + "'s"