from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def upload_to(instance, filename):
    return '{}/{}/{}'.format('Profile_Photo', instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Man = 'E'
    Woman = 'K'
    Other = 'O'

    GENDER = (
        (Man, 'Man'),
        (Woman, 'Woman'),
        (Other, 'Other'),
    )

    PUBLIC = 'P'
    FOLLOWING = 'F'

    VISIBLE = (
        (PUBLIC, 'PUBLIC'),
        (FOLLOWING, 'FOLLOWING'),
    )

    phone_number = models.CharField(max_length=11, verbose_name='Telefon Numarası', blank=True)

    gender = models.CharField(max_length=1, default=3, verbose_name='Cinsiyet', choices=GENDER, blank=True)

    bio = models.TextField(max_length=500, verbose_name='Hakkında', blank=True)

    date_birth = models.DateField(blank=True, verbose_name='Doğum Tarihi', null=True)

    profile_photo = models.ImageField(upload_to=upload_to, verbose_name='Profil Foto', blank=True)

    visible = models.CharField(max_length=1, default=1, verbose_name="Profil Durumu", choices=VISIBLE)

    class Meta:
        verbose_name = 'Kullanıcı Bilgileri'
        verbose_name_plural = 'Kullanıcı Bilgileri'

    def get_full_name_or_username(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.get_username()

    def __str__(self):
        return '{} Profile'.format(self.get_full_name_or_username())

    def profile_photos(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        return '/static/img/user.png'


def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# User' ın save metodu Çalışırsa receiver deki adrese git .
post_save.connect(receiver=create_user_profile, sender=User)
