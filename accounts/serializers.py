from rest_framework import serializers


class VerifySmsCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True, min_value=100000, max_value=999999)
