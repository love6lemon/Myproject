from django.shortcuts import render, redirect, HttpResponse
from . import models, asset_handler
from . import forms
import hashlib, datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404

# Create your views here.
def hash_code(s, salt= 'mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.Confirmstring.objects.create(code=code, user=user,)
    return code

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自小白科技www.xiaobai.com的注册确认邮件'

    text_content = '''感谢注册www.xiaobai.com，这里是小白科技专注Python、人工智能和机器学习！\
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                        <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.xiaobai.com</a>，\
                        这里是小白科技专注于Python、人工智能和机器学习！</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.Confirmstring.objects.get(code=code)
    except:
        message = '无效的确认请求！！'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期，请重新注册！！！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！！！'
        return render(request, 'login/confirm.html', locals())



def index(request):
    if not request.session.get('is_login', None):
        return redirect('/loginn/')
    user1 = request.session.get('user_id', None)
    #7为数据库中数据表user1中的id
    if user1 == 7:
        assets = models.Asset.objects.all()
    else:
        assets = models.Asset.objects.filter(user1=user1)
    return render(request, 'login/index.html', locals())

def dashboard(request):
    user1 = request.session.get('user_id', None)
    # 7为数据库中数据表user1中的id
    if user1 == 7:
        assets = models.Asset.objects.all()
    else:
        assets = models.Asset.objects.filter(user1=user1)

    total = assets.count()
    upline = assets.filter(status=0).count()
    offline = assets.filter(status=1).count()
    unknown = assets.filter(status=2).count()
    breakdown =assets.filter(status=3).count()
    backup = assets.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)
    server_number = assets.filter(asset_type='server').count()
    networkdevice_number = assets.filter(asset_type='networkdevice').count()
    storagedevice_number = assets.filter(asset_type='storagedevice').count()
    securitydevice_number = assets.filter(asset_type='securitydevice').count()
    software_number = assets.filter(asset_type='software').count()
    return render(request, 'login/dashboard.html', locals())

def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'login/detail.html', locals())

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.Userform(request.POST)
        message = '请检查填写的内容！！！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User1.objects.get(name=username)
            except:
                message = '用户名不存在！'
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:
                message = '用户还未进行邮件注册确认!!!'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码错误，请重新输入！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.Userform()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.Registerform(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:
                message = '输入的密码不一致！'
                return render(request, 'login/register.html', locals())
            else:
                same_user = models.User1.objects.filter(name=username)
                if same_user:
                    message = '用户名已经存在！'
                    return render(request, 'login/register.html', locals())
                same_email = models.User1.objects.filter(email=email)
                if same_email:
                    message = '该邮箱已被注册！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User1()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行注册确认！！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.Registerform()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/loginn/')
    request.session.flush()
    return redirect('/loginn/')

@csrf_exempt
def report(request):
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        if not data:
            return HttpResponse('没有数据！！')

        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式！！！')
        sn = data.get('sn', None)
        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('资产数据已更新')
            else:
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse('没有资产sn序列号，请检查数据！')

    return HttpResponse('200  OK')