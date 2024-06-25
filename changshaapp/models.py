from django.db import models
from django.contrib.auth.models import User

from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types['DateTimeField'] = 'datetime' # fix for MySQL 5.5

'''
python3 manage.py makemigrations
python3 manage.py migrate changshaapp
'''

# Create your models here.
# Manager
class Participant(models.Model):
    # 和django自带的User类进行一对一关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)

# Declarant
class Declarant(models.Model):
    # 和django自带的User类进行一对一关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)

class Authentication(models.Model):
    # 发起认证请求用户的用户名
    username = models.CharField(max_length=255)
    # 发起认证请求用户上传的认证资料存储在后端的地址（只有上传成功后才新增信息）
    file = models.URLField(max_length=255, blank=True)
    # 待审核 已通过（发放认证码） 已拒绝
    authState = models.CharField(max_length=255)
    # 所发放的认证码
    authCode = models.CharField(max_length=255)