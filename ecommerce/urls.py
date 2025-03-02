from django.contrib import admin
from django.urls import path,include
from ecommerce import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('store/',include('store.urls')),
    
    path('register/',views.register, name='register'),
    path('signin/',views.signin, name='signin'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)