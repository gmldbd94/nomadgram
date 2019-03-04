from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import models

class ExploreUsers(APIView):

    def get(self, request, format=None):
        # 최근회원가입순으로 정령이 된다
        last_five = models.User.objects.all().order_by('date_joined').reverse()[:5]

        serializer = serializers.ListUserSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)

        user.save()

        return Response(status=status.HTTP_200_OK)


class unFollowUser(APIView):

    def post(self, request, user_id, format=None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)

        user.save()

        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):

    def get(self, request, username, format=None):

        try: found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListFollowUser(APIView):
    def get(self, rquest, username, format=None):

        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followers = found_user.followers.all()

        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListFollowingUser(APIView):

    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_followings = found_user.following.all()
        serializer = serializers.ListUserSerializer(user_followings, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

#
# def UserFollowingFBV(request, username):
#
#     if request.method == 'GET':
#         try:
#             found_user = models.User.objects.get(username=username)
#         except models.User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         user_following = found_user.following.all()
#
#         serializer = serializers.ListUserSerializer(user_following, many=True)
#
#         return Response(data=serializer.data, status=status.HTTP_200_OK)

class Search(APIView):

    def get(self, request, format=None):

        username = request.query_params.get('username', None)

        if username is not None:

            users = models.User.objects.filter(username__istartwith=username)

            serializer = serializers.ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:

            return Response(status=status.HTTP_400_BAD_REQUEST_NO_CONTENT)
