from django.db import models
from nomadgram.users import models as user_models
from taggit.managers import TaggableManager

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 메타는 실제 필드값이 아니다
    class Meta:
        abstract=True

class Image(TimeStampedModel):

    """Image Model"""
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='images')
    tags = TaggableManager()

    # property는 종속된 함수를 작성할 때 사용한다고 보면 된다.
    # like숫자를 함수를 작성해준 것이다.
    @property
    def likes_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        # 생성된 날짜순으로 정령
        ordering = ['-created_at']

class Comment(TimeStampedModel):

    """Commnet Model"""
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self):
        return self.message


class Like(TimeStampedModel):

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='likes')

    def __str__(self):
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption)

