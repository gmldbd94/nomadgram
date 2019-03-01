#
from django.shortcuts import render

#엘리먼트를 가져오고 method를 관리하는 멋진 클래스이다.
from rest_framework.response import Response
from rest_framework.views import APIView

from faker import Faker
from . import models, serializers
import random
from nomadgram.users import models as user_model


class faker_image(APIView):
    def get(self, request, format=None):
        myfake = Faker()
        user = user_model.User.objects.all()
        image = models.Image.objects.create(file="https://2runzzal.com/media/VG9ubjh2UjlRWk9Cay81RzBBSzNndz09/zzal.jpg",
                                            location=myfake.company(),
                                            caption=myfake.sentences(),
                                            creator=random.choice(user))
        serializer = serializers.ImageSerializer(image, many=True)
        return Response(status=200)

class faker_comment(APIView):
    def get(self, request, format=None):
        myfake = Faker()
        user = user_model.User.objects.all()
        image = models.Image.objects.all()
        comment = models.Comment.objects.create(
            message = myfake.text(),
            creator = random.choice(user),
            image = random.choice(image),
        )
        return Response(status=200)

# my Faker의 매소드를 통해 어떤 종류의 가짜데이터를 뽑아낼지 결정가능


# Create your views here.
# class ListAllImages(APIView):
#
#     def get(self, request, format=None):
#         #format 은 json, xml이 될수 있다.
#
#         all_images = models.Image.objects.all()
#
#         #image시리얼 라이져는 단수이다. 그래서 여러개의 이미지를 불러오기 위해서 many-True 값을 넣어줘야한다.
#         serializer = serializers.ImageSerializer(all_images, many=True)
#
#         return Response(data=serializer.data)
#
# class ListAllComments(APIView):
#
#     def get(self, request, format=None):
#         user_id = request.user.id
#         all_comments = models.Comment.objects.all()
#
#         serializer = serializers.CommentSerializer(all_comments, many=True)
#
#         return Response(data=serializer.data)
#
# class ListAllLikes(APIView):
#
#     def get(self, request, format=None):
#
#         all_likes = models.Like.objects.all()
#
#         serializer = serializers.LikeSerializer(all_likes, many=True)
#
#         return Response(data=serializer.data)


class Feed(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            # images -> foriegn키를 받는 대상을 related_name통하여 images로 변경하였다.
            # [:2]는 모델 리스트를 제한하는 방법이다.
            user_images = following_user.images.all()[:2]

            for image in user_images:
                # 이미지를 각각 image배열에 추가하여라
                image_list.append(image)

            print(image_list)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        # sorted_list = sorted(image_list, key=get_key, reverse=True)
        # 아래 주석친 부분과 함께 사용한 것과 같은 맥락이다.
        print(sorted_list)

        serializer = serializers.ImageSerializer(sorted_list, many="True")
        return Response(data=serializer.data)

# def get_key(image):
#     return image.created_at
