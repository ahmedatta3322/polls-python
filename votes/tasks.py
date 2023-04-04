from django.core.mail import send_mail
from celery import shared_task
from polls.models import Votes
@shared_task
def send_daily_email():
    subject = 'Daily email'
    number_of_votes_today = Votes.objects.filter(created_at__date=timezone.now().date()).count()
    message = 'Number of votes today: ' + str(number_of_votes_today)
    from_email = 'youremail@example.com'
    recipient_list = ['recipient1@example.com', 'recipient2@example.com']
    send_mail(subject, message, from_email, recipient_list)