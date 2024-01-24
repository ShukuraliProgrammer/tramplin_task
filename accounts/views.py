from django.core.cache import cache
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import serializers, status

from accounts.serializers import VerifySmsCodeSerializer
from accounts.crud import get_profile
from accounts.management.commands.run_bot import bot


# Create your views here.
class VerifySmsCodeView(CreateAPIView):
    """
    This view checks user's verification code and if it's valid, then it activates user's profile
    :param code: verification code
    :return: user's data
    """
    queryset = None
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            code = serializer.validated_data.get("code")
            data = cache.get(code)
            print("data", data)
            if data is None:
                return Response({"message": "code_was_invalid_or_expired"},
                                status=status.HTTP_400_BAD_REQUEST)

            user_data = bot.get_chat(data)
            print("user_data", user_data)
            profile = get_profile(user_data.username)

            if profile is False:
                return Response({"message": "profile_not_found"},
                                status=status.HTTP_404_NOT_FOUND)

            profile.is_active = True
            profile.save(update_fields=["is_active"])
            data = {
                "user_id": profile.user_id,
                "username": profile.username,
                "phone": profile.phone
            }

            return Response({"message": "OK", "data": data}, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            return Response({"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
