from rest_framework import serializers
from . import models

class CommentSerializer(serializers.ModelSerializer):

    # imgae = ImageSerializer()

    class Meta:
        model = models.Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    # image = ImageSerializer()

    class Meta:
        model = models.Like
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta: #설정하는 클래스
        model = models.Image


        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'likes',
        )



