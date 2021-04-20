from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import User
import datetime
import pytz
from django.conf import settings
from apps.decorators import login_required, superuser_required, anonymous_required, superuser_only
from django.contrib.auth.hashers import make_password
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

"""
func: 登录
"""


class LoginView(View):
    @anonymous_required
    def get(self, request):
        login_form = UserForm()
        return render(request, 'account/templates/account/login.html', locals())

    @anonymous_required
    def post(self, request):
        login_form = UserForm(data=request.POST)
        if login_form.is_valid():
            if User.objects.filter(username=login_form.cleaned_data['username']):
                user = authenticate(username=login_form.cleaned_data['username'],
                                    password=login_form.cleaned_data['password'])
                if user:
                    login(request, user)
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    # Todo: check if is super user
                    # request.session['is_superuser'] = user.is_superuser
                    return HttpResponse("LoginSuccess")
                else:
                    message = "密码不正确"
                    return HttpResponse("LoginDenied")
            else:
                message = "用户不存在"
        else:
            message = "未知错误"
        login_form = UserForm()
        return render(request, 'account/templates/account/login.html', locals())


"""
func: 登出
"""


class LogoutView(View):
    @login_required(login_url=settings.LOGIN_REDIRECT_URL)
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('login')


"""
func: 注册
"""


class RegisterView(View):
    @anonymous_required
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'account/templates/account/register.html', locals())

    @anonymous_required
    def post(self, request):
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同!"
                return render(request, 'account/templates/account/register.html', locals())
            same_name_user = User.objects.filter(username=username)
            if same_name_user:  # 用户名唯一
                message = '用户已经存在，请重新选择用户名!'
                return render(request, 'account/templates/account/register.html', locals())
            try:
                password = make_password(password1)
                user = User.objects.create(username=username, password=password, is_superuser=False, email=email)
                user.save()
                message = "注册成功"
                login_form = UserForm()
                return render(request, 'account/templates/account/login.html', locals())  # 自动跳转到登录页面
            except:
                message = "注册失败,请稍后重试"
                return render(request, 'account/templates/account/register.html', locals())
        message = "验证码错误"
        register_form = RegisterForm()
        return render(request, 'account/templates/account/register.html', locals())


"""
func: 登录状态下修改密码
"""


class ChangePasswordLogin(View):
    @login_required
    def get(self, request, message=None):
        user_pass_form = UserPassChangeForm()
        return render(request, "account/templates/account/change_pass.html", locals())

    @login_required
    def post(self, request):
        userPassForm = UserPassChangeForm(data=request.POST)
        message = None
        if userPassForm.is_valid():
            old_password = userPassForm.cleaned_data['oldpassword']
            user_password1 = userPassForm.cleaned_data['password1']
            user_password2 = userPassForm.cleaned_data['password2']
            if user_password1 == user_password2 and request.user.check_password(old_password):
                user = User.objects.filter(username=request.user.username)
                user.set_password(user_password1)
                user.save()
                LogoutView.get(request)
                return redirect(reverse("account:login"))
            elif user_password1 != user_password2:
                message = "密码不一致"
            else:
                message = "密码错误"
        return self.get(request, message=message)


"""
func: 非登录状态修改密码
"""


class ChangePasswordUnLoginName(View):
    @anonymous_required
    def get(self, request, message=None):
        user_name_form = UserNameForm()
        return render(request, "account/templates/account/input_name.html", locals())

    @anonymous_required
    def post(self, request):
        userNameForm = UserNameForm(request.POST)
        message = None
        if userNameForm.is_valid():
            username = userNameForm['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if user:
                request.session['user_set_name'] = user.username
                serializer = Serializer(settings.SECRET_KEY, 120)
                info = {'confirm': user.username}
                token = serializer.dumps(info)  # bytes
                token = token.decode('utf8')
                # TODO: Post email
                self.call_post_mail(user, token, user.email)
                return HttpResponse("The link has been sent, please enter your configured mail to confirm")
            else:
                message = "用户名不存在"
        user_name_form = UserNameForm()
        return render(request, "account/templates/account/input_name.html", locals())

    def call_post_mail(self, user: User, token, email):
        from django.core.mail import EmailMultiAlternatives
        subject = '密码确认邮件'
        text_content = '''如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员!'''
        html_content = '''
                                <p>{username}感谢使用</p>
                                <p>请返回站点链接完成修改密码确认！</p>
                                <p>您的验证id为<a href=\"http://127.0.0.1:8000/account/pass/{token}\">
                                \"http://127.0.0.1:8000/user/active/{token}\"
                                </a></p>
                                <p>此链接有效期为2min！</p>
                                '''.format(username=user.username, token=token)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class ChangePasswordUnLoginToken(View):
    @anonymous_required
    def get(self, request, token=None):
        if token:
            serializer = Serializer(settings.SECRET_KEY, 3600)
            try:
                info = serializer.loads(token)
                # 获取待激活用户的id
                username = info['confirm']
                if request.session['user_set_name'] and username == request.session['user_set_name']:
                    try:
                        user = User.objects.get(username=username)
                        request.session['user_set_allowed'] = True
                        return redirect(reverse("account:change_pass_anonymous_pass"))
                    except User.DoesNotExist:
                        message = "用户不存在"
                else:
                    message = "Alert"
            except SignatureExpired as e:
                return HttpResponse("失效的激活链接")
            except BadSignature as b:
                return HttpResponse("Invalid token")
        else:
            if request.session['user_set_allowed']:
                user_pass_form = UserPassForm()
                return render(request, "account/templates/account/input_new_pass.html", locals())
            else:
                return HttpResponse("Not allowed to enter")

    @anonymous_required
    def post(self, request):
        if request.session['user_set_allowed']:
            userPassForm = UserPassForm(data=request.POST)
            if userPassForm.is_valid():
                password1 = userPassForm['password1']
                password2 = userPassForm['password2']
                if password1 == password2:
                    username = request.session['username']
                    user = User.objects.get(username=username)
                    user.set_password(password1)
                    user.save()
                    return redirect(reverse("account:login"))
                else:
                    message = "Unsynchronized Password"
                    return render(request, "account/templates/account/input_new_pass.html", locals())
        else:
            return HttpResponse("Not allowed to change")
