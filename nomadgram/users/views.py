from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import models

class ExploreUsers(APIView):

    def get(self, request, format=None):
        # 최근회원가입순으로 정령이 된다
        last_five = models.User.objects.all().order_by('date_joined').reverse()[:5]

        serializer = serializers.ExploreUserSerializer(last_five, many=True)

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
