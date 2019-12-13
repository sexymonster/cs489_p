from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('practice/', views.practice, name='practice'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('post/', views.post_list, name='post_list'),
    path('post/select/<int:pk>/', views.post_detail2, name='post_detail2'),
    # path('post/<int:upk>/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/practice', views.post_practice, name='post_practice')
]