from django.urls import path

from . import views

urlpatterns = [
    # path('images/', views.ListAllImages.as_view(), name='all_images'),
    # path('comments/', views.ListAllComments.as_view(), name='all_comments'),
    # path('likes/', views.ListAllLikes.as_view(), name='all_likes'),

    # 인스타글을 보기위한 경로
    path('feed/', views.Feed.as_view(), name='feed'),

    #게시글 CRUD 경로
    path('<int:image_id>/like/', views.LikeImage.as_view(), name="like_image"),


    # 가짜데이터생성하기위한 경로
    path('fake_image/', views.faker_image.as_view(), name="fake_image"),
    path('fake_comment/', views.faker_comment.as_view(), name="fake_comment"),
]


