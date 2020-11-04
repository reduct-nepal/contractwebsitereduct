from django.contrib import admin
from django.urls import path,include
from django.urls import path
from .import views

from django.contrib.auth import views as auth_views


urlpatterns=[
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('',views.logout,name='logout'),
    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('profile/',views.profile,name='profile'),
    path('image_upload', views.hotel_image_view, name='image_upload'),
    path('success', views.success, name='success'),
    path('addcontract/',views.addcontract,name='addcontract'),
    path('showcontract/',views.showcontract,name='showcontract'),
    path('<int:iod>/update/',views.contractupdate,name='contractupdate'),
    path('<int:iod>/delete/',views.contractdelete,name='contractdelete'),
    path('<int:iod>/renew/',views.contractrenew,name='contractrenew'),
    path('<int:iod>/clause/', views.clause, name='clause'),


    path('hotel_images', views.display_hotel_images, name = 'hotel_images'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reductcontract/password_reset.html"),
         name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reductcontract/password_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reductcontract/password_reset_form.html'),
         name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reductcontract/password_reset_done.html'),
         name='password_reset_complete'),


]


