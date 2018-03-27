from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse

from posts.models import Post
from .forms import Register, LoginForm, UserProfileForm, UserProfileEdit
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .forms import UserPasswordChangeForm, UserUploadPhotoForm, UserProfileVisibleForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('posts_list'))

    form = Register(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)

        password = form.cleaned_data['password']
        new_user.set_password(password)
        new_user.save()
        super_user = authenticate(username=new_user, password=password)
        print(password)
        print(new_user)
        if super_user:
            login(request, new_user)
            return HttpResponseRedirect(reverse('posts_list'))

    return render(request, 'users/register.html', context={'form': form})


@login_required(login_url='/user/login/')
def user_change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request, user)
            messages.success(request, 'Tebrikler Şifreniz Değişti.')
    return render(request, 'users/password_change.html', context={'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('posts_list'))

    _next_ = request.GET.get('next', None)
    print(_next_)
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():

        # if next == '':
        #     _next_ = None
        _user_ = form.cleaned_data['username']
        _password_ = form.cleaned_data['password']

        super_user = authenticate(username=_user_, password=_password_)

        if super_user:
            # user = User.objects.get(username=_user_, password=_password_)
            login(request, super_user)
            print('a')
            return HttpResponseRedirect(reverse('posts_list'))
            # if _next_:
            #     print(_next_)
            #     print('merhaba')
            #     return HttpResponseRedirect(reverse('posts_list'))
            #
            #     # return HttpResponseRedirect(reverse('posts_list'))
        else:
            error_message = 'Lütfen Kullanıcı Adı veya Şifreyi Doğru Giriniz.'
            print(_next_)
            return render(request, 'users/user_login.html',
                          context={'form': form, 'error_message': error_message, 'next': _next_})

    return render(request, 'users/user_login.html', context={'form': form, 'next': _next_})


def user_logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('posts_list'))

    logout(request)
    return HttpResponseRedirect(reverse('posts_list'))


@login_required(login_url='/user/login/')
def edit_user_profile(request):
    data = {
        'gender': request.user.profile.gender,
        'bio': request.user.profile.bio,
        'date_birth': request.user.profile.date_birth,
        'phone_number': request.user.profile.phone_number
    }
    user_profile_form = UserProfileForm(request.POST or None, instance=request.user, initial=data)

    if request.method == 'POST':
        if user_profile_form.is_valid():
            user_profile_form.save(commit=True)

            # bio = user_profile_form.cleaned_data['bio']
            # phone_number = user_profile_form.cleaned_data['phone_number']
            # date_birth = user_profile_form.cleaned_data['date_birth']
            # gender = user_profile_form.cleaned_data['gender']
            #
            # request.user.profile.bio = bio
            # request.user.profile.phone_number = phone_number
            # request.user.profile.date_birth = date_birth
            # request.user.profile.gender = gender

            user_edit_form = UserProfileEdit(data=request.POST, instance=request.user.profile)
            user_edit_form.save(commit=True)

            request.user.profile.save()

            messages.success(request, 'Kullanıcı Bilgileriniz Başarıyla Güncellendi')
            return HttpResponseRedirect(reverse('posts_list'))

    return render(request, 'users/user_edit_profile.html', context={'form': user_profile_form})


def user_upload_photo(request):
    if request.method == 'POST':
        form = UserUploadPhotoForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=True)

            data = \
                {
                    'is_valid': True,
                    'img-url': user_profile.profile_photo.url,
                    'success': 'Profil Fotoğrafınız Başaralı Bir Şekilde Güncellendi'
                }
            return JsonResponse(data=data)
        else:
            return JsonResponse(data={'is_valid': False})
    else:
        return HttpResponseRedirect(reverse('edit_profile'))


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        print(user.profile.visible)
    form = UserProfileVisibleForm(instance=user.profile)
    post_list = Post.objects.filter(user=user)
    return render(request, 'users/user_profile.html',
                  context={'post_list': post_list, 'user': user, 'form': form})


@login_required(login_url='/user/login/')
def user_visible(request):
    data = {}
    if request.method == "POST":
        profile = request.user.profile
        form = UserProfileVisibleForm(data=request.POST, instance=profile)
        profile = form.save(commit=True)
        data = {'visible': profile.visible}
    return JsonResponse(data)
