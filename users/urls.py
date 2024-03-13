from django.urls import path
from .views import SignUpView, VerifyApiView, ResendVerifyView

urlpatterns =[
    path('signup/', SignUpView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('resend_verify/', ResendVerifyView.as_view()),
]