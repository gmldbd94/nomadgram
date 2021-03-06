#
from django.shortcuts import render

#엘리먼트를 가져오고 method를 관리하는 멋진 클래스이다.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from nomadgram.notification import views as notification_views
from faker import Faker

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
        images = models.Image.objects.all()
        random_image = random.choice(images)
        comment = models.Comment.objects.create(
            message=myfake.text(),
            image=random_image,
            creator=random_image.creator,
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


class LikeImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(pk=image_id)

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #try문을 진행하고 만약 except 조건과 같은 문제라면 except문을 실행한다.

        try:
            new_like = found_image.likes.get(creator=user)
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        # except found_image.DoesNotExist:
        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image,
            )
            new_like.save()

            notification_views.create_notification(user, found_image.creator, 'like', found_image)

        # try문을 통하여 좋아요가 존재하는지 확인하고 만약 존재하지 않는다면 except문이 실행된다.
            return Response(status=status.HTTP_201_CREATED)


class unLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(pk=image_id)

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):


    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


        serializer = serializers.CommentSerializer(data=request.data)

        #serializer이 잘 작동하는지 확인해보는 것이다.
        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)
            print("correct serializer")

            notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'])

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            print("Bad request")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 만약 csrf에러가 뜬다면 setting에서 보안을 해지애햐한다.


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtag', None)

        if hashtags is not None:

            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImagesSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_204_NO_CONTENT)
        # deep_ralationship을 검색하는 기능
        # title: 'hello',
        # location: 'bogota',
        # creator: (User:
        #           id:1,
        #           username:'nomadmin'
        #           )
        # 위와 같은 테이블에서 'noma'라는 문자열이 포환된 값을 검색할 떄
        # models.Image.objects.filter(creator_username_contains='noma')
        #icontains 은 소문자대분자를 구분하지 않고 검색한다.
        #iexact 은 정확히 일치하는 값을 검색
