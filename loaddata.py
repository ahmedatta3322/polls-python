import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votes.settings')
import django
django.setup()

from polls.models import Poll, Choice, Vote
from django.contrib.auth.models import User



# generate users , random users 

import random
import time
users = []
for i in range(1, 1000):
    user = User.objects.create_user(username=f"user{i}", password=f"password{i}")
    users.append(user)
    print(f"User {i} created")

# generate polls , random polls
polls = []
for i in range(1, 1000):
    # generate random date
    expiration_date = time.strftime("%Y-%m-%d", time.gmtime())
    poll = Poll.objects.create(question=f"Question {i}", expiration_date=expiration_date , created_by=random.choice(users))
    polls.append(poll)
    print(f"Poll {i} created")

# generate choices , random choices
choices = []
for i in range(1, 1000):
    # generate random poll
    poll = random.choice(polls)
    choice = Choice.objects.create(choice_text=f"Choice {i}", poll=poll)
    choices.append(choice)
    print(f"Choice {i} created")
# save all to db
User.objects.bulk_create(users)
Poll.objects.bulk_create(polls)
Choice.objects.bulk_create(choices)




    