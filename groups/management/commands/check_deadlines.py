from datetime import date
from django.core.management.base import BaseCommand
from django.urls import reverse
from groups.models import CustomGroup
from accounts.models import Notification

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        active_groups_leaders = CustomGroup.objects.filter(closed=False).select_related('leader')
        for current_group in active_groups_leaders:
            if current_group.deadline < date.today():
                new_notification = Notification(
                    user=current_group.leader,
                    type='ETC',
                    context_user=current_group.leader,
                    content=(
                        f'The deadline has past for the group ' 
                        f'''<a href="{reverse('group_members', kwargs={'pk': current_group.id})}">{current_group.name}</a>.'''
                        f'''<br>You can now <a href="{reverse('select_assignment', kwargs={'group_id': current_group.id})}">'''
                        f'assign wishlists</a> at any time!')
                )
                new_notification.save()