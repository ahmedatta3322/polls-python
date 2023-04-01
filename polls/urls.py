from django.urls import path
from .views import PollCreateView , PollUpdateView, PollDeleteView , PollListView, PollDetailView
from .views import ChoiceCreateView, ChoiceUpdateView, ChoiceDeleteView, ChoiceListView, ChoiceDetailView
from .views import VoteView
urlpatterns = [
    path('poll/create/', PollCreateView.as_view(), name='create'),
    path('poll/update/<int:pk>/', PollUpdateView.as_view(), name='update'),
    path('poll/delete/<int:pk>/', PollDeleteView.as_view(), name='delete'),
    path('poll/list/', PollListView.as_view(), name='list'),
    path('poll/view/<int:pk>/', PollDetailView.as_view(), name='detail'),
    path('choice/create/', ChoiceCreateView.as_view(), name='choice_create'),
    path('choice/update/<int:pk>/', ChoiceUpdateView.as_view(), name='choice_update'),
    path('choice/delete/<int:pk>/', ChoiceDeleteView.as_view(), name='choice_delete'),
    path('choice/list/', ChoiceListView.as_view(), name='choice_list'),
    path('choice/view/<int:pk>/', ChoiceDetailView.as_view(), name='choice_detail'),
    path('vote/', VoteView.as_view(), name='vote'),

]


