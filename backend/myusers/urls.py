from django.urls import path
from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    path("login/", views.login_view),
    path("signup/", views.signup_view),
    path("test-token/", views.test_token_view),
]
