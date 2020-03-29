"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from portfolioApp.models import User, Item, Review, List
from django.conf.urls.static import static
from django.conf import settings

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
class ItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(Item, ItemAdmin)
class ReviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Review, ReviewAdmin)
class ListAdmin(admin.ModelAdmin):
    pass
admin.site.register(List, ListAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolioApp.urls'))
]

# routes to serve up media and static files, do something else in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

