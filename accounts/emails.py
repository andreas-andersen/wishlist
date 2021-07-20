from django.http import HttpRequest
from django.contrib.auth.forms import PasswordResetForm

def reset_invited_user_password(
        receiving_user, 
        inviting_user, 
        inviting_group,
        template='registration/invitation_email.html'
):
    form = PasswordResetForm({'email': receiving_user.email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = 'www.mydomain.com'
        request.META['SERVER_PORT'] = '443'
        form.save(
            request=request,
            use_https=True,
            html_email_template_name=template,
            extra_email_context={
                'inviting_user': inviting_user,
                'inviting_group': inviting_group,
            }
        )