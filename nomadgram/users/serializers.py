from rest_framework import serializers
from . import models
from nomadgram.images import serializers as images_serializers

class UserProfileSerializer(serializers.ModelSerializer):
    images = images_serializers.CountImagesSerializer(many=True)

    class Meta:
        model = models.User
        fields = (
            'username',
            'name',
            'website',
            'bio',
            'post_count',
            'followers_count',
            'following_count',
            'images',

        )
class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
            'followers_count',
            'following_count',
        )


