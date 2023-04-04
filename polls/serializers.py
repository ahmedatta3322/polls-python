from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from .models import Poll, Choice , Vote
from django.contrib.auth.models import User
from django.utils import timezone



class PollSerializer(ModelSerializer):
    choices = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    class Meta:
        model = Poll
        fields = ('id', 'question', 'expiration_date','choices', 'voted' , 'total_votes' , 'is_expired')
    
    def create(self, validated_data) -> Poll:
        """
        Create a new poll.
        """
        user_id = self.context['created_by']
        choices = self.context['choices']
        # create choices if not None
        if choices is not None:
            poll = Poll.objects.create(created_by_id=user_id, **validated_data)
            for choice in choices:
                Choice.objects.create(poll=poll, choice_text=choice)
            return poll
        user = User.objects.get(id=user_id)
        poll = Poll.objects.create(created_by=user, **validated_data)
        return poll
    
    def update(self, instance, validated_data) -> Poll:
        """
        Update a poll.
        """
        instance.question = validated_data.get('question', instance.question)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        # update choices
        choices = self.context['choices']
        if choices is not None:
            # delete old choices
            print(choices)
            Choice.objects.filter(poll=instance).delete()
            # create new choices
            for choice in choices:
                print(choice.get("choice_text"))
                Choice.objects.create(poll=instance, choice_text=choice.get("choice_text"))

        instance.save()
        return instance
    def get_choices(self, obj):
        # filter choices by poll
        choices = Choice.objects.filter(poll=obj)
        return ChoiceSerializer(choices, many=True).data
    
    def get_voted(self, obj):
        user_id = self.context['user_id']
        filter_votes = Vote.objects.filter(poll=obj.id , voted_by=user_id)
        return filter_votes.count() > 0
    
    def get_total_votes(self, obj):
        filter_votes = Vote.objects.filter(poll=obj.id)
        return filter_votes.count()
    def get_is_expired(self, obj):
        return obj.expiration_date < timezone.now()
    


class ChoiceSerializer(ModelSerializer):
    votes_count = serializers.SerializerMethodField()
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'votes_count', 'poll')

    def get_votes_count(self, obj):
        filter_votes = Vote.objects.filter(choice=obj.id)
        return filter_votes.count()


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'choice','poll')

    def create(self, validated_data) -> Vote:
        """
        Create a new vote.
        """
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id)
        poll = validated_data['choice'].poll
        if poll.expiration_date < timezone.now():
            raise serializers.ValidationError('The poll has expired.')
        if poll.id != validated_data['poll'].id:
            raise serializers.ValidationError('The choice is not part of the poll.')
        # don't allow the user to vote twice
        filter_votes = Vote.objects.filter(poll=poll.id, voted_by=user_id)
        if filter_votes.count() > 0:
            raise serializers.ValidationError('You have already voted.')
        vote = Vote.objects.create(voted_by=user, **validated_data)
        return vote

        