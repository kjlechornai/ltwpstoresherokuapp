from django.urls import path
from rest_framework.authtoken import views
from .views import ItemAPIView, ReceiveAPIView, IssueAPIView, NewReceiveAPIView, NewIssueAPIView

app_name = 'api'

urlpatterns = [
    path('', ItemAPIView.as_view(), name='items'),
    path('api-auth-token', views.obtain_auth_token, name='api-auth-token'),
    path('<str:name>', ItemAPIView.as_view(), name='filter'),
    path('receive/', ReceiveAPIView.as_view(), name='receive'),
    path('issue/', IssueAPIView.as_view(), name='issue'),
    path('new-receive/', NewReceiveAPIView.as_view(), name='new-receive'),
    path('new-issue/', NewIssueAPIView.as_view(), name='new-issue'),
]