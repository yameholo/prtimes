from django.db import models


class Message(models.Model):
    text = models.CharField("text", max_length=255)
    company_id = models.SlugField("company_id")
    release_id = models.SlugField("release_id")
    created_at = models.DateTimeField("created_at", auto_now_add=True)
