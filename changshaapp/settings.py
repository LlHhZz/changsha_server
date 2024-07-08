from django.http import JsonResponse
from django.contrib.auth.models import User
from changshaapp.models import Participant, Declarant, Authentication, Declaration, AuthenticationExtractionStatus
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Manager 管理员
def getinfo(request):
    user = request.user
    # 若管理员还未认证，显示登录注册页面
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'failed',
            'msg': '管理员未通过身份验证',
        })
    
    # 取出管理员信息，返回
    actor = Participant.objects.all()[0]
    return JsonResponse({
        'result': 'success',
        'username': user.username,
        'photo': actor.photo,
        'phone': actor.phone,
    })

def signin(request):
    # login
    if request.method == 'POST':
        data = request.POST
        
        username = data.get('username').strip()
        password = data.get('password').strip()
        
        if not username or not password:
            return JsonResponse({
                'result': '用户名或密码不能为空',
            })

        # 根据管理员输入的username和password进行身份验证
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({
                'result': '用户名或密码不正确',
            })
        # 在Participant中查验
        if Participant.objects.filter(user=user).exists():
            # 验证成功，完成登录
            login(request, user)
            return JsonResponse({
                'result': 'success',
            })
        else:
            return JsonResponse({
                'result': '未分配管理员权限',
            })
    else:
        return JsonResponse({
            'result': '请求失败'
        })

def signout(request):
    # logout
    user = request.user
    # 若已为未验证状态，返回登出成功
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'success'
        })
    # 完成登出
    logout(request)
    return JsonResponse({
        'result': 'success'
    })

def register(request):
    # CreateNormalUser and login
    if request.method == 'POST':
        data = request.POST
        username = data.get('username', "").strip()
        password = data.get('password', "").strip()
        if not username or not password:
            return JsonResponse({
                'result': '用户名和密码不能为空'
            })
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'result': '用户名已存在'
            })
        user = User(username=username)
        user.set_password(password)
        user.save()
        try:
            Participant.objects.create(user=user, photo='https://p.qqan.com/up/2021-5/16202670881472791.jpg', phone='12312341234')
        except:
            return JsonResponse({
                'result': '授权失败'
            })
        return JsonResponse({
            'result': 'success'
        })


# Declarant 申报人 用户
def getinfo2(request):
    user = request.user
    # 若用户还未认证，显示登录注册页面
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'failed',
            'msg': '用户未通过身份验证',
        })
    
    # 取出用户信息，返回
    actor = Declarant.objects.all()[0]
    return JsonResponse({
        'result': 'success',
        'username': user.username,
        'photo': actor.photo,
        'phone': actor.phone,
    })

def getAuthInfoByUsername(request):
    # 申报人通过username获取当前的认证状态以及认证码
    if request.method == 'POST':
        data = request.POST
        username = data.get('username').strip()

        if not username:
            return JsonResponse({
                'result': '用户名不能为空',
            })

        authentication = Authentication.objects.filter(username=username, authState='已通过');
        authenticationExtractionStatus = AuthenticationExtractionStatus.objects.filter(username=username)[0];
        if authentication:
            if authenticationExtractionStatus.extractionStatus == '待提取':
                authenticationExtractionStatus.extractionStatus = '已提取'
                authenticationExtractionStatus.save()

                return JsonResponse({
                    'result': 'success',
                    'authState': '已通过',
                    'authCode': authentication[0].authCode
                })
            else:
                return JsonResponse({
                    'result': '认证码已被提取'
                })
        else:
            authentication = Authentication.objects.filter(username=username, authState='已拒绝');
            if authentication:
                return JsonResponse({
                    'result': 'success',
                    'authState': '已拒绝',
                    'authCode': '',
                })
            else:
                return JsonResponse({
                    'result': 'success',
                    'authState': '待审核',
                    'authCode': '',
                })
    else:
        return JsonResponse({
            'result': '请求失败'
        })

def signin2(request):
    # login
    if request.method == 'POST':
        data = request.POST
        print(data)
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        # 根据用户输入的username和password进行身份验证
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({
                'result': '用户名或密码不正确',
            })
        # 验证成功，完成登录
        login(request, user)
        return JsonResponse({
            'result': 'success',
        })
    else:
        return JsonResponse({
            'result': '请求失败'
        })

def signout2(request):
    # logout
    user = request.user
    # 若已为未验证状态，返回登出成功
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'success'
        })
    # 完成登出
    logout(request)
    return JsonResponse({
        'result': 'success'
    })

def register2(request):
    # CreateNormalUser and login
    if request.method == 'POST':
        data = request.POST
        username = data.get('username', "").strip()
        password = data.get('password', "").strip()
        password_confirm = data.get('password_confirm', "").strip()
        if not username or not password:
            return JsonResponse({
                'result': '用户名和密码不能为空'
            })
        if password != password_confirm:
            return JsonResponse({
                'result': '两次输入的密码不一致'
            })
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'result': '用户名已存在'
            })
        user = User(username=username)
        user.set_password(password)
        user.save()
        Declarant.objects.create(user=user, photo='https://p.qqan.com/up/2021-5/16202670881472791.jpg', phone='12312341234')
        return JsonResponse({
            'result': 'success'
        })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })

# Authentication
def auth_getinfos(request):
    user = request.user
    # 若用户还未认证，显示登录注册页面
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'failed',
            'msg': '用户未通过身份验证',
        })
    
    # 取出认证请求信息，返回
    auth_requests  = Authentication.objects.all().order_by('-id')
    auth_infos = []
    for auth in auth_requests:
        auth_infos.append({
            'id': auth.id,
            'username': auth.username,
            'file': auth.file,
            'authState': auth.authState,
            'authCode': auth.authCode if auth.authState == '已通过' else '',
        })
    return JsonResponse({
        'result': 'success',
        'authInfos': auth_infos,
    })

from django import forms
from django.core.files.storage import FileSystemStorage

class UploadForm(forms.Form):
    username = forms.CharField()
    file = forms.FileField()

def auth_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 文件存储到 MEDIA_ROOT 目录下
            file = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(form.cleaned_data['username'] + '_' + file.name, file)
            uploaded_file_url = 'http://8.148.13.44:443' + fs.url(filename)

            Authentication.objects.create(username=form.cleaned_data['username'], file=uploaded_file_url, authState='待审核', authCode='')
            
            authenticationExtractionStatus = AuthenticationExtractionStatus.objects.filter(username = form.cleaned_data['username'])
            if not authenticationExtractionStatus:
                AuthenticationExtractionStatus.objects.create(username = form.cleaned_data['username'], extractionStatus = '待提取')
            else:
                authenticationExtractionStatus = AuthenticationExtractionStatus.objects.get(username = form.cleaned_data['username'])
                authenticationExtractionStatus.extractionStatus = '待提取'
                authenticationExtractionStatus.save()

            # 返回文件 URL
            return JsonResponse({
                'result': 'success',
                'fileUrl': uploaded_file_url,
            })
        else:
            # 如果表单验证失败，返回错误信息
            return JsonResponse({
                'result': 'failed',
                'error': form.errors,
            })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })

def auth_edit(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id')
        username = data.get('username', "").strip()
        authState = data.get('authState', "").strip()
        if authState == '已通过':
            authCode = data.get('authCode', "").strip()
            if not authCode:
                return JsonResponse({
                    'result': '分配验证码不能为空'
                })
            # 使用id查找Authentication实例，这里假设Authentication是一个模型类
            try:
                authentication = Authentication.objects.get(id=id)
            except Authentication.DoesNotExist:
                return JsonResponse({
                    'result': '未找到相应的认证信息'
                })
            # 更新Authentication实例的字段
            authentication.username = username
            authentication.authState = authState
            authentication.authCode = authCode

            # 保存更改
            authentication.save()

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                # 如果用户名已存在，可以选择更新现有用户的信息或者返回错误
                user = User.objects.get(username=username)
            else:
                # 创建新用户
                user = User(username=username)
                user.set_password(authCode)
                user.save()

            try:
                Declarant.objects.create(user=user, photo='https://p.qqan.com/up/2021-5/16202670881472791.jpg', phone='12312341234')
            except:
                return JsonResponse({
                    'result': '用户创建失败'
                })

            return JsonResponse({
                'result': 'success'
            })
        elif authState == '已拒绝':
            # 使用id查找Authentication实例，这里假设Authentication是一个模型类
            try:
                authentication = Authentication.objects.get(id=id)
            except Authentication.DoesNotExist:
                return JsonResponse({
                    'result': '未找到相应的认证信息'
                })
            # 更新Authentication实例的字段
            authentication.username = username
            authentication.authState = authState

            # 保存更改
            authentication.save()

            return JsonResponse({
                'result': 'success'
            })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })

# Declaration
def declaration_getinfos(request):
    user = request.user
    # 若用户还未认证，显示登录注册页面
    if not user.is_authenticated:
        return JsonResponse({
            'result': 'failed',
            'msg': '用户未通过身份验证',
        })
    
    # 取出认证请求信息，返回
    declaration_requests  = Declaration.objects.all().order_by('-id')
    declaration_infos = []
    for declaration in declaration_requests:
        declaration_infos.append({
            'id': declaration.id,
            'username': declaration.username,
            'declarationArea': declaration.declarationArea,
            'declarationElectricity': declaration.declarationElectricity,
            'FMCapacity': declaration.FMCapacity,
            'electricityPrice': declaration.electricityPrice,
            'mileagePrice': declaration.mileagePrice,
            'capacityPrice': declaration.capacityPrice,
            'reviewState': declaration.reviewState,
        })
    return JsonResponse({
        'result': 'success',
        'declarationInfos': declaration_infos,
    })

def declaration_upload(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username', "").strip()
        declarationArea = data.get('declarationArea', "").strip()
        declarationElectricity = data.get('declarationElectricity', "").strip()
        FMCapacity = data.get('FMCapacity', "").strip()
        electricityPrice = data.get('electricityPrice', "").strip()
        mileagePrice = data.get('mileagePrice', "").strip()
        capacityPrice = data.get('capacityPrice', "").strip()
        reviewState = data.get('reviewState', "").strip()

        print(username)
        print(declarationArea)
        print(declarationElectricity)

        try:
            declaration = Declaration.objects.create(
                username=username,
                declarationArea=declarationArea,
                declarationElectricity=declarationElectricity,
                FMCapacity=FMCapacity,
                electricityPrice=electricityPrice,
                mileagePrice=mileagePrice,
                capacityPrice=capacityPrice,
                reviewState=reviewState
            )
        except Exception as e:
            return JsonResponse({
                'result': '申报提交失败',
                'error': str(e)
            }, status=400)

        return JsonResponse({
            'result': 'success',
        })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })

# 根据id删除对应的申报表项
def declaration_delete(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id', None)
        print(id)

        if(id):
            try:
                declaration = Declaration.objects.get(id=id)
                declaration.delete()
            except Exception as e:
                return JsonResponse({
                    'result': '申报删除失败',
                    'error': str(e)
                }, status=400)
        else:
            return JsonResponse({
                'result': '必须提供申报ID'
            }, status=400)

        return JsonResponse({
            'result': 'success',
        })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })

# 更新当前申报项的状态
def declaration_edit(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id')
        declarationState = data.get('declarationState', "").strip()

        print(declarationState)

        if declarationState == '已通过':
            try:
                declaration = Declaration.objects.get(id=id)
                # 更新Declaration实例的字段
                declaration.reviewState = declarationState;

                # 保存更改
                declaration.save()
            except Declaration.DoesNotExist:
                return JsonResponse({
                    'result': '未找到相应的申报信息'
                })

            return JsonResponse({
                'result': 'success'
            })
        elif declarationState == '已拒绝':
            try:
                declaration = Declaration.objects.get(id=id)
                # 更新Declaration实例的字段
                declaration.reviewState = declarationState;

                # 保存更改
                declaration.save()
            except Declaration.DoesNotExist:
                return JsonResponse({
                    'result': '未找到相应的申报信息'
                })

            return JsonResponse({
                'result': 'success'
            })
    else:
        return JsonResponse({
            'result': '请求方法错误'
        })