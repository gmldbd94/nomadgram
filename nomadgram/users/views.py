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
