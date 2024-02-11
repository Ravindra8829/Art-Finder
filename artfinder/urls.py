"""artfinder URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from orders.admin import dispatch_site
from .views import home, update_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dispatchadmin/', dispatch_site.urls),
    path('cart/', include('carts.urls', namespace='carts')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('products/', include('products.urls', namespace='products')),
    path('update-cart/', update_cart, name='update_cart'),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.index_title = 'ArtFinder'
admin.site.site_header = 'ArtFinder Admin'
admin.site.site_title = 'Control Panel'
