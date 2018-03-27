from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return '{}/{}/{}'.format('posts', instance, filename)


class Category(models.Model):
    category_name = models.CharField(max_length=120)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Kategoriler'
        verbose_name_plural = 'Kategoriler'


class PostManager(models.Manager):

    # def all(self, *args, **kwargs):
    #     return super(PostManager, self).filter(draft=False)
    #
    def activate(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)

    def draft(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=True)


class Post(models.Model):
    category = models.ManyToManyField(Category, related_name='post')

    title = models.CharField(max_length=200, blank=False, verbose_name='Başlık')

    user = models.ForeignKey(User, null=True, default=1, related_name='posts',
                             verbose_name='Kullanıcı', on_delete=models.CASCADE)

    slug = models.SlugField(max_length=500, unique=True, null=False, editable=False)

    content = RichTextField()

    img = models.ImageField(blank=True, null=True, verbose_name='Image', upload_to=upload_to, max_length=500)

    draft = models.BooleanField(default=False, verbose_name='Taslak Olutşrulsun mu ?')

    created_date = models.DateTimeField(auto_now_add=True)  # Bu ilk olutşturulduğunda

    updated_date = models.DateTimeField(auto_now=True)  # Bu her save işleminde

    objects = PostManager()

    def __str__(self):
        return '{}'.format(self.title)

    def get_image(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        return '/static/img/default.png'

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Gönderilerim'
        verbose_name_plural = 'Gönderilerim'
        ordering = ['-created_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='Post', related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='User', related_name='user_comment', on_delete=models.CASCADE)
    c_content = models.TextField(verbose_name='Yorum')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment'
        ordering = ['-date']

    def __str__(self):
        return '{} - {}'.format(self.post, self.user)


class CommentChild(models.Model):
    comment = models.ForeignKey(Comment, related_name="comment_child", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment_child', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="İçerik")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Yorumlar"
        ordering = ['-date']

    def __str__(self):
        return '{}'.format(self.comment)
