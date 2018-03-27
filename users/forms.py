from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .models import Profile


class Register(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        length = len(User.objects.filter(email=email))
        if length > 0:
            raise forms.ValidationError('Bu Email Adresi önceden kUllanılış')

        return email


class UserProfileForm(forms.ModelForm):
    Man = 'E'
    Woman = 'K'
    Other = 'O'

    GENDER = (
        (Man, 'Man'),
        (Woman, 'Woman'),
        (Other, 'Other'),
    )
    gender = forms.CharField(widget=forms.Select(choices=GENDER))
    bio = forms.CharField(widget=forms.Textarea(), max_length=500, required=False)
    date_birth = forms.DateField(widget=forms.SelectDateWidget, label='Doğum Tarihi', required=False)
    phone_number = forms.CharField(max_length=11, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_birth',
            'phone_number',
            'gender',
            'bio',
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['bio'].widget.attrs['rows'] = 10
        self.fields['bio'].widget.attrs['cols'] = 10


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class UserProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender',
            'date_birth',
            'phone_number',
            'bio',
        ]


class UserUploadPhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_photo'
        ]


class UserProfileVisibleForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'visible'
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileVisibleForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if '@' in username:
            user = User.objects.filter(email=username)
            if len(user) == 1:
                __user__ = user.first()
                return __user__.username

            elif len(user) > 1:
                raise forms.ValidationError('Lütfen Kullanıcı Adı İle Giriş Yapınız')

            else:
                raise forms.ValidationError('Böle Bir Kullanıcı\' ya Rastlanamadı ')

        return username
