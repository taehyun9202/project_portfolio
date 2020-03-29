from django.urls import path
from .import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('aboutme', views.aboutme),
    path('mywork', views.mywork),
    path('contact', views.contact),
    path('item/<itemid>',views.item),
    path('addtolist/<itemid>', views.addtolist),
    path('list', views.itemlist),
    path('list/delete/<itemid>', views.delete),
    path('list/checkout', views.checkout),
    path('edit', views.edit),
    path('update', views.update),
    path('sendemail', views.sendemail),
    path('logout', views.logout)
]