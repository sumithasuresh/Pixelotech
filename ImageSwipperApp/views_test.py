from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Image, Swipe
from .serializers import UserSerializer, ImageSerializer, SwipeSerializer


class UserSignUpViewTestCase(APITestCase):
    def test_valid_signup(self):
        url = reverse('user-signup')
        data = {'name': 'Test User', 'email': 'test@example.com', 'mobile': '1234567890', 'otp': '00000'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Test User')

    def test_invalid_otp(self):
        url = reverse('user-signup')
        data = {'name': 'Test User', 'email': 'test@example.com', 'mobile': '1234567890', 'otp': '11111'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserSignInViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='Test User', email='test@example.com', mobile='1234567890')

    def test_valid_signin(self):
        url = reverse('user-signin')
        data = {'mobile': '1234567890', 'otp': '00000'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Welcome Test User')

    def test_invalid_otp(self):
        url = reverse('user-signin')
        data = {'mobile': '1234567890', 'otp': '11111'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid OTP')


class ImageViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name='Test User', email='test@example.com', mobile='1234567890')
        self.image = Image.objects.create(name='Test Image', url='http://example.com/test.jpg')

    def test_get_images(self):
        url = reverse('image-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Image')

    def test_valid_rating(self):
        url = reverse('image-list')
        data = {'image_id': self.image.id, 'rating': 'accepted', 'user_id': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Swipe.objects.count(), 1)
        self.assertEqual(Swipe.objects.get().liked, 'accepted')
