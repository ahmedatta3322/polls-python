from rest_framework.views import APIView
from .serializers import PollSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Poll
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
        serializer = PollSerializer(data=request.data, context={'created_by': user})
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
        serializer = PollSerializer(poll, data=request.data, context={'created_by': user})
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
    
class PollListView(APIView):
    """
    View to list all polls.
    """
    def get(self, request) -> Response:
        """
        List all polls.
        """
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, status=200)
    
class PollDetailView(APIView):
    """
    View to retrieve a poll.
    """
    def get(self, request, pk) -> Response:
        """
        Retrieve a poll.
        """
        try:
            poll = Poll.objects.get(id=pk)
        except Poll.DoesNotExist:
            return Response(status=404, data={'message': 'Poll not found.'})
        serializer = PollSerializer(poll)
        return Response(serializer.data, status=200)
