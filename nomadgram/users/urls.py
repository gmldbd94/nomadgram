from django.urls import path
from . import views
# from nomadgram.users.views import (
#     user_list_view,
#     user_redirect_view,
#     user_update_view,
#     user_detail_view,
# )

app_name = "users"
urlpatterns = [
    path("explore/", views.ExploreUsers.as_view(), name="explore_user"),
    path("<int:user_id>/follow", views.FollowUser.as_view(), name="follow_user"),
    path("<int:user_id>/unfollow", views.unFollowUser.as_view(), name="unfollow_user"),
]
