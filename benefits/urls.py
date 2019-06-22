from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('customers.urls')),
    path('partner/', include('partners.urls')),
    path('account/', include('members.urls')),
    path('perks/', include('perks.urls')),
    path('', include('cms.urls')),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = settings.ADMIN_SITE_HEADER
