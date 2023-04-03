from rest_framework.views import APIView
from .serializers import PollSerializer , ChoiceSerializer , VoteSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from .models import Poll
from rest_framework import pagination
# Create your views here.

class PollCreateView(APIView):
    """
    View to create a new poll.
    """
    permission_classes = (IsAdminUser,)
    def post(self, request) -> Response:
        """
        Create a new poll.
        """
        user = request.user.id
        choices = None
        if 'choices' in request.data:
            choices = request.data.pop('choices')
        serializer = PollSerializer(data=request.data, context={'created_by': user , 'user_id': user , 'choices': choices})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class PollUpdateView(APIView):
    """
    View to update a poll.
    """
    permission_classes = (IsAdminUser,)
    def put(self, request, pk) -> Response:
        """
        Update a poll.
        """
        
        user = request.user.id
        try:
            poll = Poll.objects.get(id=pk)
        except Poll.DoesNotExist:
            return Response(status=404, data={'message': 'Poll not found.'})
        serializer = PollSerializer(poll, data=request.data, context={'created_by': user , 'user_id': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class PollDeleteView(APIView):
    """
    View to delete a poll.
    """
    permission_classes = (IsAdminUser,)
    def delete(self, request, pk) -> Response:
        """
        Delete a poll.
        """
        user = request.user.id
        try:
            poll = Poll.objects.get(id=pk)
        except Poll.DoesNotExist:
            return Response(status=404, data={'message': 'Poll not found.'})
        if poll.created_by.id == user:
            poll.delete()
            return Response(status=204 , data={'message': 'Poll deleted successfully.'})
        return Response(status=403)
    
class PollListView(APIView , pagination.PageNumberPagination):
    """
    View to list all polls.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request) -> Response:
        """
        List all polls.
        """
        user = request.user.id
        # order by expiration date so that the polls that are not expired are listed first
        polls = self.paginate_queryset(Poll.objects.all().order_by('expiration_date').reverse(), request , view=self)
        serializer = PollSerializer(polls, many=True, context={'user_id': user})
        return self.get_paginated_response(serializer.data)
    
class PollDetailView(APIView):
    """
    View to retrieve a poll.
    """
    def get(self, request, pk) -> Response:
        """
        Retrieve a poll.
        """
        user = request.user.id
        try:
            poll = Poll.objects.get(id=pk)
        except Poll.DoesNotExist:
            return Response(status=404, data={'message': 'Poll not found.'})
        serializer = PollSerializer(poll, context={'user_id': user})
        return Response(serializer.data, status=200)

class ChoiceCreateView(APIView):
    """
    View to create a new choice.
    """
    permission_classes = (IsAdminUser,)
    def post(self, request) -> Response:
        """
        Create a new choice.
        """
        user = request.user.id
        serializer = ChoiceSerializer(data=request.data, context={'created_by': user , 'user_id': user})
        if serializer.is_valid():
            serializer.save()
            context = {'user_id': user}
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ChoiceUpdateView(APIView):
    """
    View to update a choice.
    """
    permission_classes = (IsAdminUser,)
    def put(self, request, pk) -> Response:
        """
        Update a choice.
        """
        user = request.user.id
        try:
            choice = Choice.objects.get(id=pk)
        except Choice.DoesNotExist:
            return Response(status=404, data={'message': 'Choice not found.'})
        serializer = ChoiceSerializer(choice, data=request.data, context={'created_by': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class ChoiceDeleteView(APIView):
    """
    View to delete a choice.
    """
    permission_classes = (IsAdminUser,)
    def delete(self, request, pk) -> Response:
        """
        Delete a choice.
        """
        user = request.user.id
        try:
            choice = Choice.objects.get(id=pk)
        except Choice.DoesNotExist:
            return Response(status=404, data={'message': 'Choice not found.'})
        if choice.created_by.id == user:
            choice.delete()
            return Response(status=204 , data={'message': 'Choice deleted successfully.'})
        return Response(status=403)
    
class ChoiceListView(APIView):

    """
    View to list all choices.
    """
    def get(self, request) -> Response:
        """
        List all choices.
        """
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data, status=200)
    
class ChoiceDetailView(APIView):

    """
    View to retrieve a choice.
    """
    def get(self, request, pk) -> Response:
        """
        Retrieve a choice.
        """
        try:
            choice = Choice.objects.get(id=pk)
        except Choice.DoesNotExist:
            return Response(status=404, data={'message': 'Choice not found.'})
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data, status=200)
    
class VoteView(APIView):
    """
    View to create a new vote.
    """
    def post(self, request) -> Response:
        """
        Create a new vote.
        """
        user = request.user.id
        serializer = VoteSerializer(data=request.data, context={'user_id': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
