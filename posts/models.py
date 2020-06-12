import uuid

from django.db import models


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='pictures')

    def __str__(self):
        return self.title
