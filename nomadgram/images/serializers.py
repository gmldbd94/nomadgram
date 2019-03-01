from rest_framework import serializers
from . import models
from nomadgram.users import models as user_model

class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_model.User
        fields = (
            'username',
            'profile_image',
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
            'created_at',
        )

class LikeSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    # 불피요한 좋아요 내용을 주석처리하였다.
    # likes = LikeSerializer(many= True)
    creator = FeedUserSerializer()

    class Meta: #설정하는 클래스
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            # 'likes',
            'creator',
            'likes_counts',
        )



