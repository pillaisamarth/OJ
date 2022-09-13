from rest_framework import serializers

from authentication.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    username=serializers.CharField(required=True, min_length=8)
    password=serializers.CharField(required=True, min_length=10, write_only=True)

    class Meta:
        model=CustomUser
        fields=('email', 'username', 'password', 'rating')

    def create(self, validated_data):
        password=validated_data.pop('password', None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance