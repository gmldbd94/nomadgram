from django.urls import path

from . import views

urlpatterns = [
    # path('images/', views.ListAllImages.as_view(), name='all_images'),
    # path('comments/', views.ListAllComments.as_view(), name='all_comments'),
    # path('likes/', views.ListAllLikes.as_view(), name='all_likes'),

    path('feed/', views.Feed.as_view(), name='feed'),



    path('fake_image/', views.faker_image.as_view(), name="fake_image"),
    path('fake_comment/', views.faker_comment.as_view(), name="fake_comment"),
]


