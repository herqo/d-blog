from django.urls import path
from .views import index, post_create, post_delete, post_detail, post_list, post_update, add_child_comment


urlpatterns = [
    path('', post_list, name='posts_list'),
    path('create/', post_create, name='posts_create'),
    path('detail/<slug>', post_detail, name='posts_detail'),
    path('add_child_comment/<pk>', add_child_comment, name='add_child_comment'),
    path('update/<slug>', post_update, name='posts_update'),
    path('delete/<slug>', post_delete, name='posts_delete'),
]
# Eski Sürümlerde
# url(r'^update/(?P<slug>)[-\w]+/$')