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
    # 认证状态：待审核 已通过（发放认证码） 已拒绝
    authState = models.CharField(max_length=255)
    # 所发放的认证码
    authCode = models.CharField(max_length=255)

class Declaration(models.Model):
    # 发起认证请求用户的用户名
    username = models.CharField(max_length=255)
    # 申报区域（望城区等）
    declarationArea = models.CharField(max_length=255)
    # 申报电量
    declarationElectricity = models.FloatField()
    # 调频容量
    FMCapacity = models.FloatField()
    # 电量价格
    electricityPrice = models.FloatField()
    # 里程价格
    mileagePrice = models.FloatField()
    # 容量价格
    capacityPrice = models.FloatField()
    # 审核状态（待审核，通过，未通过）
    reviewState = models.CharField(max_length=255)

class AuthenticationExtractionStatus(models.Model):
    # 认证用户名
    username = models.CharField(max_length=255)
    # 提取状态：待提取 已提取（约束：只允许根据用户名提取一次）
    # 再重新通过用户名和认证材料申报后，重新发放认证码后，允许再次提取新的认证码
    extractionStatus = models.CharField(max_length=255)

class Data(models.Model):
    # 上传数据的用户名
    username = models.CharField(max_length=255)
    # 数据处理完成后保存的路径
    file = models.URLField(max_length=255, blank=True)