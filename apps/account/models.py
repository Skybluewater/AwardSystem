from django.db import models
from django.contrib.auth.models import AbstractUser
from database.base_model import BaseModel

# Create your models here.


class User(AbstractUser):
    student_id = models.CharField(max_length=10)
    isPostgraduate = models.BooleanField(default=False)


class ConfirmString(models.Model):
    '''
    确认code类
    '''
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
