from django.urls import path

from accounts.views import VerifySmsCodeView

urlpatterns = [
    path("verify-code/", VerifySmsCodeView.as_view(), name="verify"),
]
