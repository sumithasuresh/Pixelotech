from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from .models import User, Image, Swipe
from .serializers import UserSerializer, ImageSerializer, SwipeSerializer


class UserSignUpView(APIView):
    def post(self, request, format=None):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')

        if otp == "00000":
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class UserSignInView(APIView):
    def post(self, request, format=None):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')

        if otp == '00000':
            user = User.objects.get(mobile=mobile)
            serializer = UserSerializer(user)
            return Response({'message': f"Welcome {serializer.data['name']}"},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):
    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        image_id = request.data.get('image_id')
        rating = request.data.get('rating')
        user_id = request.data.get('user_id')

        if rating not in ['accepted', 'rejected']:
            return Response({'message': 'Invalid rating'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.objects.get(id=image_id)
            user = User.objects.get(id=user_id)
        except (Image.DoesNotExist, User.DoesNotExist):
            return Response({'message': 'Invalid image or user'}, status=status.HTTP_400_BAD_REQUEST)

        rating_obj = Swipe(image=image, user=user, rating=rating)
        rating_obj.save()

        return Response({'message': f"{user.name}, you have {rating} image {image.name}"}, status=status.HTTP_201_CREATED)


class HistoryView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            ratings = Swipe.objects.filter(user=user)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SwipeSerializer(ratings, many=True)
        return Response(serializer.data)
