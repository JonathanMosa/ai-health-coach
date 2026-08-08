from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView
from .views import CheckInRetrieveUpdateDestroyView, CheckInListCreateView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", obtain_auth_token, name="login"),
    path("checkins/", CheckInListCreateView.as_view(), name="checkin-list"),
    path("checkins/<int:pk>/", CheckInRetrieveUpdateDestroyView.as_view(), name="checkin-detail"),
]
