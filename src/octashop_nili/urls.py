from django.conf.urls import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings


admin_urls = [
    path('api/admin/catalogs/', include(('apps.catalogs.urls.admin','apps.catalogs'), namespace='catalogs-admin')),
]
front_urls = [
    path('api/front/catalogs/', include(('apps.catalogs.urls.front','apps.catalogs'), namespace='catalogs-front')),
]

doc_urls = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


site_urls = [
    path('', include(('apps.home.urls','apps.home'), namespace='home-site')),
    path('api/site/catalogs/', include(('apps.catalogs.urls.site', 'apps.catalogs'), namespace='catalogs-site')),
    path('auth/', include(('auth.users.urls.site','auth.users'), namespace='users-site')),
    path('api/site/cart/', include(('apps.cart.urls.site','apps.cart'), namespace='cart-site')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
] + admin_urls + front_urls + doc_urls + site_urls


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_title = "OctaShop - NiliTeb"
admin.site.site_header = "OctaShop - NiliTeb"
admin.site.index_title = "OctaShop - NiliTeb"