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
    path("search/", views.Search.as_view(), name="user_search"),
    path("<int:user_id>/follow", views.FollowUser.as_view(), name="follow_user"),
    path("<int:user_id>/unfollow", views.unFollowUser.as_view(), name="unfollow_user"),
    path("<str:username>/profile", views.UserProfile.as_view(), name="UserProfile"),
    path("<str:username>/followers", views.ListFollowUser.as_view(), name="ListFollowers"),
    path("<str:username>/followings", views.ListFollowingUser.as_view(), name="ListFollowings"),

]
