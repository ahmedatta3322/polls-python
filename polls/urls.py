from django.urls import path
from .views import PollCreateView , PollUpdateView, PollDeleteView , PollListView, PollDetailView

urlpatterns = [
    path('create/', PollCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PollUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PollDeleteView.as_view(), name='delete'),
    path('list/', PollListView.as_view(), name='list'),
    path('view/<int:pk>/', PollDetailView.as_view(), name='detail'),

]


