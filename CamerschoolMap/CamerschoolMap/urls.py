
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpattern
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CamerSchool.urls')),   
    path('login/', include('login.urls')),   
    path('login/', include('add_school.urls')),   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += staticfiles_urlpattern()
