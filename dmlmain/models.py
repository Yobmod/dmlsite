from django.db import models


class SignUp(models.Model):
    email: models.EmailField = models.EmailField()
    name: models.CharField = models.CharField(max_length=200, blank=True, null=True)
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated: models.DateTimeField = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return str(self.email)
