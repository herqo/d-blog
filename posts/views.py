from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import Http404
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.shortcuts import HttpResponse

from . import is_owner
from .forms import PostForm, PostFilterForm, CommentFrom
from .models import Post, CommentChild, Comment

from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponseRedirect(reverse('posts_list'))


def post_list(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('q', None)

    filter_form = PostFilterForm(request.GET or None)
    post__list = Post.objects.all()

    if filter_form.is_valid():
        option = filter_form.cleaned_data['option']

        if option == 'D':
            post__list = Post.objects.draft()

        elif option == 'ND':
            post__list = Post.objects.activate()

        elif option == 'A':
            post__list = post__list.all()

        else:
            raise Http404
    if search:
        post__list = post__list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(category__category_name__icontains=search)
        )

    paginator = Paginator(post__list, 10)

    try:
        post__list = paginator.page(page)
    except PageNotAnInteger:
        post__list = paginator.page(1)
    except EmptyPage:
        post__list = paginator.page(paginator.num_pages)

    return render(request, 'post/post_list.html', context={'post_list': post__list, 'filter_form': filter_form})


@login_required(login_url='/user/login/')
def post_create(request, current_user=None):
    # Cleaned Data = Kullanıcının yazdığı bölümleri kısıtlamak (En az 8 harf)
    # request.user.is_authenticated = current_user
    if not request.user.is_authenticated:
        raise Http404

    post_form = PostForm()
    print(reverse('posts_list'))
    if request.method == 'POST':

        post_form = PostForm(request.POST, files=request.FILES)

        if post_form.is_valid():  # Hazırladığımız Cleaned Datalara uyuyor mu diye
            created_post = post_form.save(commit=False)
            created_post.user = request.user
            created_post.save()
            messages.success(request, 'Post Oluşturuldu')
            return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': created_post.slug}))
            # detay sayfasına yönlendirme de kwargs paramteri ile belirtmeliyiz

    return render(request, 'post/post_create.html', context={'form': post_form})


def post_detail(request, slug):
    # post = Post.objects.get slug=slug)
    post = get_object_or_404(Post, slug=slug)

    comment_form = CommentFrom(request.POST or None)

    if request.method == "POST":
        if comment_form.is_valid():
            if request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                comment_form = CommentFrom()
                messages.success(request, 'Yorum Birazdan Yayınlanır')
                return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': post.slug}))
            else:
                return messages.error(request, 'Lütfen Önce Giriş Yapınız', extra_tags='danger')
    return render(request, 'post/detail.html', context={'post_list': Post.objects.all(), 'form': comment_form})


@login_required(login_url='/user/login/')
def add_child_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == "POST":
        user = request.user
        content = request.POST['c_content']
        CommentChild.objects.create(user=user, comment=comment, content=content)

    return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': comment.post.slug}))


@login_required(login_url='/user/login/')
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    answer = is_owner(post, request.user)
    if not answer:
        messages.error(request, 'Lütfen Size Ait Olmayan Postları Güncellemeye Çalışmayın.', extra_tags='danger')
        return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': post.slug}))

    form = PostForm(data=request.POST or None, instance=post, files=request.FILES or None)

    if form.is_valid():
        form.save(commit=True)

        messages.success(request, 'Post Başarılı Bir Şekilde Güncellendi')
        return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': form.instance.slug}))
    return render(request, 'post/post_update.html', context={'form': form})


@login_required(login_url='/user/login/')
def post_delete(request, slug):
    # if request.method == 'POST':
    #     slug = request.POST.get('post_id', None)
    #     post = get_object_or_404(Post, slug=slug)
    #     print('merhaba')
    #     post.delete()
    #     return HttpResponseRedirect(reverse('posts_list'))

    if not request.user.is_authenticated:
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    answer = is_owner(post, request.user)
    if not answer:
        messages.error(request, 'Lütfen Size Ait Olmayan Postları Silmeye Çalışmayın.', extra_tags='danger')
        return HttpResponseRedirect(reverse('posts_detail', kwargs={'slug': post.slug}))

    post.delete()
    messages.success(request, 'Post Silindi', extra_tags='danger')
    return HttpResponseRedirect(reverse('posts_list'))
