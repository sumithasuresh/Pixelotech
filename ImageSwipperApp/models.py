from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Swipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'image')

    def __str__(self):
        return f"{self.user.name} {'liked' if self.liked else 'disliked'} {self.image.name}"
