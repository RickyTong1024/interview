from django.contrib.auth import authenticate, login
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用户',
        min_length=4,
        max_length=16,
        error_messages={'required':'必选项'}
    )

    password = forms.CharField(
        required=True,
        label='密码',
        min_length=4,
        max_length=16,
        widget=forms.PasswordInput,
        error_messages={'required':'必选项'}
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            #如果成功返回对应的User对象，否则返回None(只是判断此用户是否存在，不判断是否is_active或者is_staff)
            if self.user_cache is None:
                raise forms.ValidationError(u"您输入的用户名或密码不正确!")
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u"您输入的用户名或密码不正确!")
            else:
                login(self.request,self.user_cache)
                self.request.session.set_expiry(10800)
        return self.cleaned_data
