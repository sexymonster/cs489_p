from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('practice/', views.practice, name='practice'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('post/', views.post_list, name='post_list'),
    # path('post/<int:upk>/', views.post_list, name='post_list'),

    path('post/new/', views.post_new, name='post_new'),
    path('post/theme_new/', views.theme_new, name='theme_new'),
    path('post/<str:theme>/delete/', views.theme_delete, name='theme_delete'),
    path('post/<str:theme>/change/', views.theme_change, name='theme_change'),
    path('post/<str:theme>/', views.post_list_theme, name='post_list_theme'),
    path('post/<str:theme>/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<str:theme>/<int:pk>/delete/',views.post_delete,name='post_delete'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/practice', views.post_practice, name='post_practice')
]