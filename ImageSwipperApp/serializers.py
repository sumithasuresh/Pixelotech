from rest_framework import serializers
from .models import User, Image, Swipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' #('id', 'name', 'mobile')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'image')


class SwipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Swipe
        fields = ('id', 'user', 'image', 'liked', 'timestamp')
