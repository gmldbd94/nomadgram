from django.db import models
from nomadgram.users import models as user_models
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

