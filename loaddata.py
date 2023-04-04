import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votes.settings')
import django
django.setup()

from polls.models import Poll, Choice, Vote
from django.contrib.auth.models import User



# generate users , random users 

import random
import time
from django.utils import timezone

users = []
#generate 1000 users
# for i in range(1000):
#     username = "user" + str(i)
#     user = User.objects.create_user(username=username, email=username + "@gmail.com", password="password")
#     user.save()
#     users.append(user)
#     print("user created: " + username)

#generate 100 random polls , for each poll generate 2-5 random choices , some of them expired, generate some votes for each poll with different created_at dates
for i in range(100):
    question = "question" + str(i)
    start_date = timezone.now() + timezone.timedelta(days=random.randint(-100, 0))
    end_date = timezone.now() + timezone.timedelta(days=random.randint(1, 100))
    expiration_date = random.choice([start_date, end_date])
    users = User.objects.all()
    created_by = random.choice(users)
    poll = Poll.objects.create(question=question, expiration_date=expiration_date, created_by=created_by)
    poll.save()
    print("poll created: " + question)
    for j in range(random.randint(2, 5)):
        choice_text = "choice" + str(j)
        choice = Choice.objects.create(poll=poll, choice_text=choice_text)
        choice.save()
        print("choice created: " + choice_text)
        # generate some votes for each choice
        for k in range(random.randint(0, 10)):
            voted_by = random.choice(users)
            created_at = timezone.now() + timezone.timedelta(days=random.randint(-100, 0))
            vote = Vote.objects.create(poll=poll, choice=choice, voted_by=voted_by, created_at=created_at)
            vote.save()
            print("vote created: " + choice_text)

