from rest_framework.serializers import ModelSerializer
from .models import Poll, Choice
from django.contrib.auth.models import User

class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'question', 'expiration_date')
    
    def create(self, validated_data) -> Poll:
        """
        Create a new poll.
        """
        user_id = self.context['created_by']
        user = User.objects.get(id=user_id)
        poll = Poll.objects.create(created_by=user, **validated_data)
        return poll
    
    def update(self, instance, validated_data) -> Poll:
        """
        Update a poll.
        """
        instance.question = validated_data.get('question', instance.question)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.save()
        return instance

class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'votes', 'poll')